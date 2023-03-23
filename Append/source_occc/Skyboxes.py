from module_info import *

sf_day        = 0x00000000
sf_dawn       = 0x00000001
sf_night      = 0x00000002
sf_mask       = 0x00000003  ## CC-D add: stop call from game

sf_clouds_0   = 0x00000000
sf_clouds_1   = 0x00000010
sf_clouds_2   = 0x00000020
sf_clouds_3   = 0x00000030

sf_no_shadows = 0x10000000
sf_HDR        = 0x20000000

# mesh_name, flags, sun_heading, sun_altitude, flare_strength, postfx, sun_color, hemi_color, ambient_color, (fog_start, fog_color),

skyboxes = [

  ("skybox_cloud_1", sf_day|sf_clouds_1, 179.0, 52.0, 0.85, "pfx_sunny", (1.39*1.32,1.39*1.21,1.39*1.08), (0.0, 0.0, 0.0), (0.96*16.0/255,0.96*23.5/255,0.96*44.5/255), (300, 0xFF8CA2AD)),
  ("skybox_cloud_1", sf_day|sf_clouds_1|sf_HDR, 179.0, 52.0, 0.85, "pfx_sunny", (1.39*1.32,1.39*1.21,1.39*1.08), (0.0, 0.0, 0.0), (0.86*16.0/255,0.86*23.5/255,0.86*44.5/255), (300, 0xFF8CA2AD)),

  ("skybox_night_1", sf_night|sf_clouds_1, 152.0, 38.0, 0.0, "pfx_night", (1.0*17.0/255,1.0*21.0/255,1.0*27.0/255),(0.0,0.0,0.0), (0.9*5.0/255,0.9*5.0/255,0.9*15.0/255), (500, 0xFF152035)),
  ("skybox_night_1", sf_night|sf_clouds_1|sf_HDR, 152.0, 38.0, 0.0, "pfx_night", (1.0*17.0/255,1.0*21.0/255,1.0*27.0/255),(0.0,0.0,0.0), (0.9*5.0/255,0.9*5.0/255,0.9*15.0/255), (500, 0xFF152035)),
  ("skybox_night_2", sf_night|sf_clouds_3, 152.0, 38.0, 0.0, "pfx_night", (1.0*17.0/255,1.0*21.0/255,1.0*27.0/255),(0.0,0.0,0.0), (0.9*5.0/255,0.9*5.0/255,0.9*15.0/255), (500, 0xFF152035)),
  ("skybox_night_2", sf_night|sf_clouds_3|sf_HDR, 152.0, 38.0, 0.0, "pfx_night", (1.0*17.0/255,1.0*21.0/255,1.0*27.0/255),(0.0,0.0,0.0), (0.9*5.0/255,0.9*5.0/255,0.9*15.0/255), (500, 0xFF152035)),
  
  ("skybox_sunset_1", sf_dawn|sf_clouds_1, 180.0, 9.146, 0.7, "pfx_sunset", (230.0/220,120.0/220,37.0/220),(0.0,0.0,0.0), (14.5/210,21.0/210,40.0/210), (150, 0xFF897262)),
  ("skybox_sunset_1", sf_dawn|sf_clouds_1|sf_HDR, 180.0, 9.146, 0.7, "pfx_sunset", (230.0/220,120.0/220,37.0/220),(0.0,0.0,0.0), (14.5/210,21.0/210,40.0/210), (150, 0xFF897262)),
  
  ("skybox_cloud_2", sf_day|sf_clouds_2, 180.0, 19.17, 0.4, "pfx_cloudy", (0.8*0.9,0.8*0.85,0.8*0.75),(0.0,0.0,0.0), (0.8*40.0/255,0.8*46.5/255,0.8*77.0/255), (120, 0xFF607090)),
  ("skybox_cloud_2", sf_day|sf_clouds_2|sf_HDR, 180.0, 19.17, 0.4, "pfx_cloudy", (0.8*0.9,0.85*0.8,0.8*0.75),(0.0,0.0,0.0), (0.8*40.0/255,0.8*46.5/255,0.8*77.0/255), (120, 0xFF607090)),
  
  ("skybox_cloud_2", sf_day|sf_clouds_3|sf_no_shadows, 180.0, 19.17, 0.4, "pfx_overcast", (0.4,0.35,0.31),(0.0,0.0,0.0), (50.0/255,60.0/255,103.0/255), (120, 0xFF607090)),
  ("skybox_cloud_2", sf_day|sf_clouds_3|sf_no_shadows|sf_HDR, 180.0, 19.17, 0.4, "pfx_overcast", (0.4,0.35,0.31),(0.0,0.0,0.0), (50.0/255,60.0/255,103.0/255), (120, 0xFF607090)),
  
  ("skybox_clearday", sf_day|sf_clouds_0, 179.0, 68.0, 0.95, "pfx_sunny", (0.99*1.32,0.99*1.21,0.99*1.08), (0.0, 0.0, 0.0), (0.96*16.0/255,0.96*23.5/255,0.96*44.5/255), (300, 0xFF8CA2AD)),  ## CC-D 80->68
  ("skybox_clearday", sf_day|sf_clouds_0|sf_HDR, 179.0, 68.0, 0.95, "pfx_sunny", (0.99*1.32,0.99*1.21,0.99*1.08), (0.0, 0.0, 0.0), (0.86*16.0/255,0.86*23.5/255,0.86*44.5/255), (300, 0xFF8CA2AD)),  ## CC-D 80->68
## CC-D begin: from polished skyboxes
  ("skybox_clear_01", sf_day|sf_clouds_1, 179.0, 52.0, 0.9, "pfx_sunny", (1.39*1.32,1.39*1.21,1.39*1.08), (0.0, 0.0, 0.0), (0.96*16.0/255,0.96*23.5/255,0.96*44.5/255), (300, 0xFF8CA2AD)),
  ("skybox_clear_01", sf_day|sf_clouds_1|sf_HDR, 179.0, 52.0, 0.9, "pfx_sunny", (1.39*1.32,1.39*1.21,1.39*1.08), (0.0, 0.0, 0.0), (0.96*16.0/255,0.96*23.5/255,0.96*44.5/255), (300, 0xFF8CA2AD)),
  #("skybox_cloud_13", sf_day|sf_clouds_1|sf_HDR, 179.0, 52.0, 0.91, "pfx_sunny", (1.39*1.32,1.39*1.21,1.39*1.08), (0.0, 0.0, 0.0), (0.86*16.0/255,0.86*23.5/255,0.86*44.5/255), (300, 0xFF8CA2AD)),  ## CC-D del: use native cloud_1
  ("skybox_cloud_03", sf_day|sf_clouds_1, 179.0, 52.0, 0.91, "pfx_sunny", (1.39*1.32,1.39*1.21,1.39*1.08), (0.0, 0.0, 0.0), (0.86*16.0/255,0.86*23.5/255,0.86*44.5/255), (300, 0xFF8CA2AD)),
  ("skybox_cloud_03", sf_day|sf_clouds_1|sf_HDR, 179.0, 52.0, 0.91, "pfx_sunny", (1.39*1.32,1.39*1.21,1.39*1.08), (0.0, 0.0, 0.0), (0.86*16.0/255,0.86*23.5/255,0.86*44.5/255), (300, 0xFF8CA2AD)),

  #("skybox_night_02", sf_night|sf_clouds_3, 152.0, 38.0, 0.0, "pfx_night", (1.0*17.0/255,1.0*21.0/255,1.0*27.0/255),(0.0,0.0,0.0), (0.9*5.0/255,0.9*5.0/255,0.9*15.0/255), (500, 0xFF152035)),  ## CC-D del: use native night_1
  #("skybox_night_02", sf_night|sf_clouds_3|sf_HDR, 152.0, 38.0, 0.0, "pfx_night", (1.0*17.0/255,1.0*21.0/255,1.0*27.0/255),(0.0,0.0,0.0), (0.9*5.0/255,0.9*5.0/255,0.9*15.0/255), (500, 0xFF152035)),  ## CC-D del: use native night_1
  #("skybox_night_01", sf_night|sf_clouds_1, 152.0, 38.0, 0.0, "pfx_night", (1.0*17.0/255,1.0*21.0/255,1.0*27.0/255),(0.0,0.0,0.0), (0.9*5.0/255,0.9*5.0/255,0.9*15.0/255), (500, 0xFF152035)),  ## CC-D del: use native night_2
  #("skybox_night_01", sf_night|sf_clouds_1|sf_HDR, 152.0, 38.0, 0.0, "pfx_night", (1.0*17.0/255,1.0*21.0/255,1.0*27.0/255),(0.0,0.0,0.0), (0.9*5.0/255,0.9*5.0/255,0.9*15.0/255), (500, 0xFF152035)),  ## CC-D del: use native night_2
  ("skybox_night_03", sf_night|sf_clouds_1, 152.0, 38.0, 0.0, "pfx_night", (1.0*17.0/255,1.0*21.0/255,1.0*27.0/255),(0.0,0.0,0.0), (0.9*5.0/255,0.9*5.0/255,0.9*15.0/255), (500, 0xFF152035)),  ## CC-D: light up st Native level
  ("skybox_night_03", sf_night|sf_clouds_1|sf_HDR, 152.0, 38.0, 0.0, "pfx_night", (1.0*17.0/255,1.0*21.0/255,1.0*27.0/255),(0.0,0.0,0.0), (0.9*5.0/255,0.9*5.0/255,0.9*15.0/255), (500, 0xFF152035)),  ## CC-D: light up st Native level

  ("skybox_sunset_01", sf_dawn|sf_clouds_1, 180.0, 9.146, 0.7, "pfx_sunset", (230.0/220,120.0/220,37.0/220),(0.0,0.0,0.0), (14.5/210,21.0/210,40.0/210), (150, 0xFF897262)),
  ("skybox_sunset_01", sf_dawn|sf_clouds_1|sf_HDR, 180.0, 9.146, 0.7, "pfx_sunset", (230.0/220,120.0/220,37.0/220),(0.0,0.0,0.0), (14.5/210,21.0/210,40.0/210), (150, 0xFF897262)),
  ("skybox_sunset_02", sf_dawn|sf_clouds_1, 180.0, 9.146, 0.7, "pfx_sunset", (230.0/220,120.0/220,37.0/220),(0.0,0.0,0.0), (14.5/210,21.0/210,40.0/210), (150, 0xFF897262)),
  ("skybox_sunset_02", sf_dawn|sf_clouds_1|sf_HDR, 180.0, 9.146, 0.7, "pfx_sunset", (230.0/220,120.0/220,37.0/220),(0.0,0.0,0.0), (14.5/210,21.0/210,40.0/210), (150, 0xFF897262)),
  #("skybox_sunset_03", sf_dawn|sf_clouds_1, 180.0, 9.146, 0.7, "pfx_sunset", (230.0/220,120.0/220,37.0/220),(0.0,0.0,0.0), (14.5/210,21.0/210,40.0/210), (150, 0xFF897262)),  ## CC-D del :black cloud
  ("skybox_sunset_04", sf_dawn|sf_clouds_1, 225.5, 2.0, 0.7, "pfx_sunset", (230.0/220,120.0/220,37.0/220),(0.0,0.0,0.0), (14.5/210,21.0/210,40.0/210), (150, 0xFF897262)),
  ("skybox_sunset_04", sf_dawn|sf_clouds_1|sf_HDR, 225.5, 2.0, 0.7, "pfx_sunset", (230.0/220,120.0/220,37.0/220),(0.0,0.0,0.0), (14.5/210,21.0/210,40.0/210), (150, 0xFF897262)),
  ("skybox_sunset_05", sf_dawn|sf_clouds_1, 167.5, 0.5, 0.7, "pfx_sunset", (230.0/220,120.0/220,37.0/220),(0.0,0.0,0.0), (14.5/210,21.0/210,40.0/210), (150, 0xFF897262)),
  ("skybox_sunset_05", sf_dawn|sf_clouds_1|sf_HDR, 167.5, 0.5, 0.7, "pfx_sunset", (230.0/220,120.0/220,37.0/220),(0.0,0.0,0.0), (14.5/210,21.0/210,40.0/210), (150, 0xFF897262)),
  #("skybox_sunset_06", sf_dawn|sf_clouds_1|sf_HDR, 180.0, 9.146, 0.7, "pfx_sunset", (230.0/220,120.0/220,37.0/220),(0.0,0.0,0.0), (14.5/210,21.0/210,40.0/210), (150, 0xFF897262)),  ## CC-D del: string cloud, double sun
  #("skybox_sunset_07", sf_dawn|sf_clouds_1|sf_HDR, 180.0, 9.146, 0.7, "pfx_sunset", (230.0/220,120.0/220,37.0/220),(0.0,0.0,0.0), (14.5/210,21.0/210,40.0/210), (150, 0xFF897262)),  ## CC-D del: use native sunset_1

  ("skybox_cloud_08", sf_day|sf_clouds_2, 169.5, 36.0, 0.4, "pfx_cloudy", (0.99*1.32,0.99*1.21,0.99*1.08), (0.0, 0.0, 0.0), (0.96*16.0/255,0.96*23.5/255,0.96*44.5/255), (300, 0xFF8CA2AD)),
  ("skybox_cloud_08", sf_day|sf_clouds_2|sf_HDR, 169.5, 36.0, 0.4, "pfx_cloudy", (0.99*1.32,0.99*1.21,0.99*1.08), (0.0, 0.0, 0.0), (0.96*16.0/255,0.96*23.5/255,0.96*44.5/255), (300, 0xFF8CA2AD)),
  #("skybox_cloud_02", sf_day|sf_clouds_2, 288.0, 62.0, 0.4, "pfx_cloudy", (0.8*0.9,0.85*0.8,0.8*0.75),(0.0,0.0,0.0), (0.8*40.0/255,0.8*46.5/255,0.8*77.0/255), (120, 0xFF607090)),  ## CC-D del: like aurora but cant only use at north land
  #("skybox_cloud_09", sf_day|sf_clouds_2, 210.0, 30.0, 0.4, "pfx_cloudy", (0.8*0.9,0.8*0.85,0.8*0.75),(0.0,0.0,0.0), (0.8*40.0/255,0.8*46.5/255,0.8*77.0/255), (120, 0xFF607090)),  ## CC-D del: double sun light area
  ("skybox_cloud_01", sf_day|sf_clouds_2, 85.0, 50.0, 0.2, "pfx_cloudy", (0.99*1.32,0.99*1.21,0.99*1.08), (0.0, 0.0, 0.0), (0.8*40.0/255,0.8*46.5/255,0.8*77.0/255), (120, 0xFF607090)),
  ("skybox_cloud_01", sf_day|sf_clouds_2|sf_HDR, 85.0, 50.0, 0.2, "pfx_cloudy", (0.99*1.32,0.99*1.21,0.99*1.08), (0.0, 0.0, 0.0), (0.8*40.0/255,0.8*46.5/255,0.8*77.0/255), (120, 0xFF607090)),
  ("skybox_cloud_06", sf_day|sf_clouds_2, 180.0, 59.0, 0.4, "pfx_cloudy", (0.8*0.9,0.8*0.85,0.8*0.75),(0.0,0.0,0.0), (0.8*40.0/255,0.8*46.5/255,0.8*77.0/255), (120, 0xFF607090)),
  ("skybox_cloud_06", sf_day|sf_clouds_2|sf_HDR, 180.0, 59.0, 0.4, "pfx_cloudy", (0.8*0.9,0.8*0.85,0.8*0.75),(0.0,0.0,0.0), (0.8*40.0/255,0.8*46.5/255,0.8*77.0/255), (120, 0xFF607090)),

  ("skybox_cloud_04", sf_day|sf_clouds_3|sf_no_shadows, 4.5, 29.5, 0.36, "pfx_overcast", (0.4,0.35,0.31),(0.0,0.0,0.0), (50.0/255,60.0/255,103.0/255), (120, 0xFF607090)),
  ("skybox_cloud_04", sf_day|sf_clouds_3|sf_no_shadows|sf_HDR, 4.5, 29.5, 0.36, "pfx_overcast", (0.4,0.35,0.31),(0.0,0.0,0.0), (50.0/255,60.0/255,103.0/255), (120, 0xFF607090)),
  ("skybox_cloud_05", sf_day|sf_clouds_3|sf_no_shadows, 316.5, 44.5, 0.38, "pfx_overcast", (0.4,0.35,0.31),(0.0,0.0,0.0), (50.0/255,60.0/255,103.0/255), (120, 0xFF607090)),
  ("skybox_cloud_05", sf_day|sf_clouds_3|sf_no_shadows|sf_HDR, 316.5, 44.5, 0.38, "pfx_overcast", (0.4,0.35,0.31),(0.0,0.0,0.0), (50.0/255,60.0/255,103.0/255), (120, 0xFF607090)),
  ("skybox_cloud_07", sf_day|sf_clouds_3|sf_no_shadows, 157.0, 45.0, 0.39, "pfx_overcast", (0.4,0.35,0.31),(0.0,0.0,0.0), (50.0/255,60.0/255,103.0/255), (120, 0xFF607090)),
  ("skybox_cloud_07", sf_day|sf_clouds_3|sf_no_shadows|sf_HDR, 157.0, 45.0, 0.39, "pfx_overcast", (0.4,0.35,0.31),(0.0,0.0,0.0), (50.0/255,60.0/255,103.0/255), (120, 0xFF607090)),
  #("skybox_cloud_10", sf_day|sf_clouds_3|sf_no_shadows|sf_HDR, 180.0, 19.17, 0.33, "pfx_overcast", (0.4,0.35,0.31),(0.0,0.0,0.0), (50.0/255,60.0/255,103.0/255), (120, 0xFF607090)),  ## CC-D del: black cloud, rough texture
  #("skybox_cloud_11", sf_day|sf_clouds_3|sf_no_shadows, 200.0, 17.0, 0.3, "pfx_overcast", (0.4,0.35,0.31),(0.0,0.0,0.0), (50.0/255,60.0/255,103.0/255), (120, 0xFF607090)),  ## CC-D del: too high border of horizon
  #("skybox_cloud_12", sf_day|sf_clouds_3|sf_no_shadows|sf_HDR, 180.0, 19.17, 0.39, "pfx_overcast", (0.4,0.35,0.31),(0.0,0.0,0.0), (50.0/255,60.0/255,103.0/255), (120, 0xFF607090)),  ## CC-D del :use native cloud_2

  #("skybox_clear_02", sf_day|sf_clouds_0, 286.5, 44.5, 1.05, "pfx_sunny", (0.99*1.32,0.99*1.21,0.99*1.08), (0.0, 0.0, 0.0), (0.96*16.0/255,0.96*23.5/255,0.96*44.5/255), (300, 0xFF8CA2AD)),  ## CC-D del: 100% blue sky, use native clearday
  #("skybox_clear_02", sf_day|sf_clouds_0|sf_HDR, 286.5, 44.5, 1.1, "pfx_sunny", (0.99*1.32,0.99*1.21,0.99*1.08), (0.0, 0.0, 0.0), (0.86*16.0/255,0.86*23.5/255,0.86*44.5/255), (300, 0xFF8CA2AD)),  ## CC-D del: 100% blue sky, use native clearday
## CC-D end
## CC-D begin
#  ("skybox_sunset_2", sf_mask|sf_no_shadows, 180.0, 90.0, 0.0, "pfx_sunset", (230.0/220,120.0/220,37.0/220),(0.0,0.0,0.0), (14.5/210,21.0/210,40.0/210), (150, 0xFF897262)),  #cant use, to move
  ("skybox_darknight", sf_mask, 152.0, 38.0, 0.0, "pfx_night", (0.1/100,0.1/100,0.1/100),(0.0,0.0,0.0), (0,0,0), (500, 0xFF101010)),
  ("skybox_darknight", sf_mask|sf_HDR, 152.0, 38.0, 0.0, "pfx_night", (0.1/100,0.1/100,0.1/100),(0.0,0.0,0.0), (0,0,0), (500, 0xFF101010)),
## CC-D end
]



def save_skyboxes():
  file = open("./skyboxes.txt","w")
  file.write("%d\n"%len(skyboxes))
  for skybox in  skyboxes:
    file.write("%s %d %f %f %f %s\n"%(skybox[0],skybox[1],skybox[2],skybox[3],skybox[4],skybox[5]))
    file.write(" %f %f %f "%skybox[6])
    file.write(" %f %f %f "%skybox[7])
    file.write(" %f %f %f "%skybox[8])
    file.write(" %f %d\n"%skybox[9])
  file.close()

print "Exporting skyboxes..."
save_skyboxes()
  
