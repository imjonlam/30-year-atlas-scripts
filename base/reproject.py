import os
from argparse import ArgumentParser
from osgeo import ogr, osr

def is_shp(parser: ArgumentParser, arg: str, meta: str) -> str:
  '''Returns arg if it is an existing shapefile'''
  if os.path.exists(arg) and arg.endswith('.shp'):
    return arg
  else:
    parser.error(f'The {meta} {arg} is invalid / does not exist')

def is_dir(parser: ArgumentParser, arg: str, meta: str) -> str:
  '''Returns arg if it is a valid directory'''
  if not os.path.isdir(arg):
    parser.error(f'The {meta} directory {arg} does not exist')
  else:
    return arg

def exists(parser: ArgumentParser, arg: str, meta: str) -> str:
  '''Returns arg if arg exists'''
  if not os.path.exists(arg):
    parser.error(f'The {meta} file {arg} does not exist')
  else:
    return arg

def main():
  parser = ArgumentParser()
  parser.add_argument('input', type=lambda x: is_shp(parser, x, 'input shapefile'), help='input shapefile')
  parser.add_argument('output', type=lambda x: is_dir(parser, x, 'output directory'), help='output directory')
  parser.add_argument('wkt', type=lambda x: exists(parser, x, 'WKT'), help='path to wkt file')
  parser.add_argument('degree', type=float, help='degree of central central meridian [-100-0]')
  args = parser.parse_args()

  # validate
  if not (-100.0 <= args.degree <= 0):
    parser.error('degree must be between [-100-0]')

  # setup
  print('setting up')
  driver = ogr.GetDriverByName('ESRI Shapefile')

  in_ds = driver.Open(args.input)
  in_layer = in_ds.GetLayer()
  in_prj = in_layer.GetSpatialRef()

  with open(args.wkt) as w:
    out_prj = osr.SpatialReference()
    out_prj.ImportFromWkt(w.read())
    out_prj.SetProjParm(osr.SRS_PP_CENTRAL_MERIDIAN, args.degree)

  if in_prj is None:
    in_ds.Release()
    in_ds = None
    raise Exception(f'ERROR: shapefile: {args.input} does not have a spatial reference')
  
  # target spatial reference is the same
  if out_prj.IsSame(in_prj):
    in_ds.Release()
    in_ds = None
    print('Input and Output projections are the same. No actions required')
    return
  
  # create new datasource
  out = os.path.join(args.output, os.path.basename(args.input))
  out_ds = driver.CreateDataSource(os.path.join(args.output, out))
  out_layer = out_ds.CreateLayer(in_layer.GetName(), out_prj, in_layer.GetGeomType())

  # transform
  coordTrans = osr.CoordinateTransformation(in_layer.GetSpatialRef(), out_prj)

  # create fields
  print('reprojecting')
  ldefn = in_layer.GetLayerDefn()
  fields = [ldefn.GetFieldDefn(n).name for n in range(ldefn.GetFieldCount())]
  for f in fields:
    i = ldefn.GetFieldIndex(f)
    if i != -1:
      fdefn = ldefn.GetFieldDefn(i)
      
      # to avoid field width errors
      if fdefn.name in ['AREA', 'PERIMETER']:
        fdefn.SetWidth(26)
        fdefn.SetPrecision(11)

      out_layer.CreateField(fdefn)
  
  # copy features
  ldefn = out_layer.GetLayerDefn()
  in_layer.ResetReading()
  for ft in in_layer:
      geom = ft.GetGeometryRef()
      geom.Transform(coordTrans)
      newFt = ogr.Feature(ldefn)
      newFt.SetGeometry(geom)

      for f in fields:
        newFt.SetField(f, ft.GetField(f))
      
      out_layer.CreateFeature(newFt)
  
  # close
  in_ds.Release()
  out_ds.Release()
  in_ds = None
  out_ds = None

  print(f'complete. Saved as: {out}')

if __name__ == "__main__":
  try:
    main()
  except Exception as e:
    print(e)
