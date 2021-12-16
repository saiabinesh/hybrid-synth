import math,sys
import airsim #pip install airsim
import numpy as np
import os
import time

# for car use CarClient() 
# client = airsim.MultirotorClient()
client = airsim.VehicleClient()
client.confirmConnection()


image_count=1
# for z in np.linspace(-30,-100,10):
    # for x in np.linspace(2.93,-37.37, 10):
        # for y in np.linspace(-88.17, -192.27,10):
yaw,pitch,roll=0,0,45

x,y,z=0,0,-6.03
number_of_objects_in_x_axis=40
x_min=190.00
y_min=-169.20
number_of_objects_in_y_axis=int(sys.argv[3]) #65
spacing=20.00
x_max=x_min + ((number_of_objects_in_x_axis-1)*spacing)
y_max=y_min + ((number_of_objects_in_y_axis-1)*spacing)
z_floor=[-1.37]
d=-(z_floor[0]+1)

start_time_actors = time.time()
location_list=[]
for z in z_floor:
    for x in np.linspace(x_min, x_max,number_of_objects_in_x_axis): 
        for y in np.linspace( y_min, y_max,number_of_objects_in_y_axis):
            location_list.append((x,y,z))

x_displacement=0
y_displacement=0

        # for z in z_floor:
            # for x in np.linspace(x_min, x_max,number_of_objects_in_x_axis): 
                # for y in np.linspace( y_min, y_max,number_of_objects_in_y_axis):

done_image_count=int(sys.argv[1])
for x_displacement in [0,d]:
    for y_displacement in [0,d]:
        for location_index in range(len(location_list)):
            # if location_index<1090 or location_index>1343:
                # image_count=image_count+1
                # continue
            
            if image_count<done_image_count:
                image_count=image_count+1
                continue
            x,y,z=location_list[location_index][0],location_list[location_index][1],location_list[location_index][2]
            # print("Setting pose")
            # print(image_count)
            one_degree_in_radians = (math.pi)/180
            if not y_displacement==0:
                roll_in_radians=math.atan(d/y_displacement)
            else: 
                roll_in_radians=0
            if not x_displacement==0:
                pitch_in_radians=math.atan(d/-x_displacement)
            else:
                pitch_in_radians=0
            yaw_in_radians=yaw * one_degree_in_radians
            client.simSetVehiclePose(airsim.Pose(airsim.Vector3r(x+x_displacement,y+y_displacement,z), airsim.to_quaternion(pitch_in_radians,roll_in_radians,yaw_in_radians)), True)
            ##########################
            folder_path='Images'
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            filename = folder_path+'/image_' +str(image_count)+'_raw' 
            png_image = client.simGetImage("3", airsim.ImageType.Scene)
            airsim.write_file(os.path.normpath(filename + '.png'), png_image) 
            if image_count%10==0:
                new_cumulative_time=(time.time() - start_time_actors)
                print("Image count: "+str(image_count)+"-Cumulative time: ",str(new_cumulative_time))

            image_count=image_count+1
            # exit()
            # unreal.SystemLibrary().collect_garbage()

            # print(image_count)
            # if image_count>=100:
                # exit()
print("Time taken to capture" + str(image_count)+" images =")
print("--- %s seconds ---" % (time.time() - start_time_actors))

                # for roll in np.linspace(-30,0,2):
                    # for pitch in np.linspace(45,0,2):
                        # for yaw in np.linspace(45,0,2):
                            # if not ((yaw==0) or (pitch == 0 and roll ==0)):
                                # continue
                            # one_degree_in_radians = (math.pi)/180
                            # pitch_in_radians=pitch * one_degree_in_radians
                            # roll_in_radians=roll * one_degree_in_radians
                            # yaw_in_radians=yaw * one_degree_in_radians
                            # # The handy `airsim.to_quaternion()` function allows to convert pitch, roll, yaw to quaternion
                            # # client.simSetCameraOrientation(0, airsim.to_quaternion(0, radians, 0)); #radians
                            # client.simSetVehiclePose(airsim.Pose(airsim.Vector3r(x,y,z), airsim.to_quaternion(pitch_in_radians,roll_in_radians,yaw_in_radians)), True)
