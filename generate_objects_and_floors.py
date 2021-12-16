import re
import sys
import unreal 
#import numpy as np
object_list =[1]
#np.random.seed(41)
import numpy as np
import random
import time
import json

def list_assets():
    list_assets=unreal.EditorAssetLibrary().list_assets(directory_path="/Game/AAA_Converted_Meshes/") 
    return list_assets

# list_assets()
# for object in object_list:
	# for scale in np.linspace(0.8,1.5,8):
		# for x in np.random.uniform(low=127, high=242, size=(10,1)):
			# for x in np.random.uniform(low=127, high=242, size=(10,1)):
				# x=2

def vector_to_list(vector):
    vector_list=[]
    vector_list.extend([vector.x,vector.y,vector.z])
    return vector_list
    

def count_all_assets_by_class(path='/Game/'): #Given a path returns a dictionary of static meshes and their counts
    asset_registry = unreal.AssetRegistryHelpers.get_asset_registry()
    all_assets = asset_registry.get_assets_by_path(path, recursive=True)
    #list_of_all_assets=list(all_assets)
    count=0
    list_of_object_paths=[]
    list_of_package_paths=list(set([str(asset.package_path) for asset in all_assets])) #Getting all the folders of classes, assuming all package paths have assets of that class ex. 
    
    print("list_of_package_paths: ", list_of_package_paths)
    
    dict_count_of_assets_by_label=dict.fromkeys(list_of_package_paths,0)
    for asset in all_assets:
        if asset.asset_class=="StaticMesh":
            dict_count_of_assets_by_label[str(asset.package_path)]+=1
            list_of_object_paths.append(str(asset.object_path))         
        #print(asset)
    #print(count)
    print("dict_count_of_assets_by_label: ",dict_count_of_assets_by_label)
    print("len(list_of_object_paths)=",len(list_of_object_paths))

    return dict_count_of_assets_by_label
    
def return_static_object_paths(master_folder): #Gets a folder inside \Game\ and returns the object paths to be used for spawning actors
    asset_registry = unreal.AssetRegistryHelpers.get_asset_registry()
    all_assets = asset_registry.get_assets_by_path(master_folder, recursive=True)
    list_of_object_paths=[]
    for asset in all_assets:
        if asset.asset_class=="StaticMesh":# or asset.asset_class=="SkeletalMesh" :
            list_of_object_paths.append(str(asset.object_path))
    print("len(list_of_object_paths)=",len(list_of_object_paths))
    # print(list_of_object_paths)
    # atlen(list_of_object_paths))
    # print(list_of_object_paths)
    return list_of_object_paths
            
def return_materials(master_folder): #Gets a folder inside \Game\ and returns the object paths to be used for spawning actors
    asset_registry = unreal.AssetRegistryHelpers.get_asset_registry()
    all_assets = asset_registry.get_assets_by_path(master_folder, recursive=True)
    list_of_object_paths=[]
    for asset in all_assets:
        # print("asset = ",asset)
        if asset.asset_class=="Material":
            list_of_object_paths.append(str(asset.object_path))    
    print("len(list_of_object_paths)=",len(list_of_object_paths))
    # print(list_of_object_paths)
    # atlen(list_of_object_paths))
    # print(list_of_object_paths)
    return list_of_object_paths

def spawn_actor_by_object_path(object_path,location_list):
    myasset = unreal.load_asset(object_path) 
    return unreal.EditorLevelLibrary().spawn_actor_from_object(myasset ,location=location_list)
    
def create_uniformly_distributed_coordinates():
    list_of_coordinates=[]
    for x in np.random.uniform(low=2000, high=4000, size=(10,1)):
        for y in np.random.uniform(low=500, high=1000, size=(10,1)):
            for z in np.random.uniform(low=500, high=1000, size=(10,1)):
                list_of_coordinates.append([x,y,z])
                
                
#Function to get center of points for creating saturation post process volumes
def sub_rectangles(lat_factor,long_factor,westlimit=0, southlimit=0, eastlimit=2, northlimit=2):
    table=list()
    #Divide the difference between the limits by the factor
    lat_adj_factor=(northlimit-southlimit)/lat_factor
    lon_adj_factor=(eastlimit-westlimit)/long_factor
    #Create longitude and latitude lists
    lat_list=[]
    lon_list=[]
    for i in range(long_factor+1):
        lon_list.append(westlimit)
        westlimit+=lon_adj_factor
    for i in range(lat_factor+1):
        lat_list.append(southlimit)
        southlimit+=lat_adj_factor
    center_list=list()
    #Build a list of longitude and latitude pairs
    for i in range(0,len(lon_list)-1):
        for j in range(0,len(lat_list)-1):
            table.append([(lon_list[i],lat_list[j]),(lon_list[i+1],lat_list[j]),(lon_list[i],lat_list[j+1]),(lon_list[i+1],lat_list[j+1])])
            min_long=min(lon_list[i],lon_list[i+1])
            max_long=max(lon_list[i],lon_list[i+1])
            min_lat=min(lat_list[j],lat_list[j+1])
            max_lat=max(lat_list[j],lat_list[j+1])
            center_list.append(((max_long+min_long)/2,(min_lat+max_lat)/2))
    # print("len(table)",len(table))
    return center_list, [lat_adj_factor, lon_adj_factor]
    
def main():
    #path1='/Game/Imports/ExportedFBX_trial'
    path1=sys.argv[1]
    object_path_list=[]
    object_path_list.append(return_static_object_paths(path1))
    # exit()
    # object_path_list.append(return_static_object_paths(path2))
    # object_path_list.append(return_static_object_paths(path3))
    # object_path_list.append(return_static_object_paths(path4))
    # new=[x.split("/")[5] for x in object_path_list[0]]
    # old=[x.split("/")[5] for x in object_path_list[1]]
    # my_list=[object_path_list[0][x] for x in range(len(new)) if not new[x] in old]

    # # my_list=[x for x in object_path_list[0] if not x in object_path_list[1]]
    my_list=[]
    for o in object_path_list[0]:
        my_list.append((o.split("/")[4]))
    # with open('D:/AirSim/UE4.24_v4/AirSim/Unreal/Environments/Blocks/Content/Python/your_filev8813.txt', 'w') as f:
        # for item in my_list:
            # f.write("%s\n" % item)
    list_of_dicts=[]
    json_dict={}
    for j in range(len(object_path_list[0])):
        json_dict[str((j+1)%len(object_path_list[0]))]=object_path_list[0][j].split("/")[4]
        # f.write("%s\n" % my_list[i])
    # THe following txt file stores the order of objects so that the different objects can be separated later.
    with open('Dict_objects.txt', 'w') as fout:
        #json.dump(json_dict, fout)
        json_string = json.dumps(json_dict, default=lambda o: o.__dict__, sort_keys=True, indent=2)
        fout.write(json_string)
    # exit()
    # # print(len(object_path_list))
    # # print(len(object_path_list[0]))
    material_path=sys.argv[2] #"/Game/Imports/floors_modify"
    material_path_list=return_materials(material_path)
    # material_path='/Game/Imports/Materials'
    # material_path_list=return_materials(material_path)
    material_path_list.insert(0,1) #prepending a 1 for no change of material
    m=len(material_path_list)
    print("len(material_path_list) =",m)
    # exit()
    if not m==10:
        exit()
    actor_count=1
    post_process_volume_list=[None]*10 #Hardcoded
    #The coordinates are hardcoded as well which should be written by another script
    number_of_objects_in_x_axis=40
    x_min=19000
    y_min=-16920
    number_of_objects_in_y_axis=int(sys.argv[3]) #65
    spacing=2000
    x_max=x_min + ((number_of_objects_in_x_axis-1)*spacing)
    y_max=y_min + ((number_of_objects_in_y_axis-1)*spacing)
    z_floor=[100]
    start_time_actors = time.time()
    # path_of_floors='/Game/Imports/NewImports'
    # floor_path_list=return_static_object_paths(path_of_floors)
    #Generating all the actors here. A total of 2160
    rotation_parameters_list=[(0,0,0),(90,0,0),(0,90,0),(0,0,90)]
    # for rotation_tuple in rotation_parameters_list:
    location_list=[]
    for z in z_floor:
        for x in np.linspace(x_min, x_max,number_of_objects_in_x_axis): 
            for y in np.linspace( y_min, y_max,number_of_objects_in_y_axis):
                location_list.append((x,y,z))
    # for saturation_contrast_count in range(6):
    # for i in range(0,4):
    object_sublist=object_path_list[0]
    done_count=1 #int(sys.argv[3])
    finish_count=10,000 #int(sys.argv[4])
    
    for rotation_tuple in rotation_parameters_list:
        for mat_path in material_path_list:
            for actor_path in object_sublist:
        
                if actor_count<done_count:
                    actor_count=actor_count+1
                    continue
                # continue
                if actor_count>finish_count:
                    print(actor_count)
                
                    exit()
                # print(location_list[actor_count-1])
                actor_1=spawn_actor_by_object_path(actor_path,location_list[actor_count-1])
                # exit()
                # print(actor_count)
                # print(location_list[actor_count-2])
                # exit()
                x,y,z=location_list[actor_count-1][0],location_list[actor_count-1][1],location_list[actor_count-1][2]
                static_mesh =actor_1.static_mesh_component.static_mesh#actor_1.static_mesh_component.static_mesh

                random_rotation=random.sample(range(-45,45), 3)
                # old_rotation_tuple=rotation_tuple
                rotation_tuple=(rotation_tuple[0]+random_rotation[0], rotation_tuple[1]+random_rotation[1], rotation_tuple[2]+random_rotation[2])
                # print(new_rotation_tuple)
                # exit()
                actor_1.set_actor_rotation(new_rotation=rotation_tuple, teleport_physics=1)
                #bounds2=static_mesh.get_bounding_box()
                half_size=actor_1.get_actor_bounds(0)[1] #returns [0] - origina nad [1] extent - half the size
                size=half_size * 2
                max_dim=max(size.x,size.y)
                #Adjust  the dimesions even further based on the new height . then multiply by height factor  to reduce the apparent width and length                
                scale=[(20/max_dim)*((z_floor[0]-(size.z*20/max_dim))/z_floor[0])]*3
                actor_1.set_actor_scale3d(scale)# print(actor_1.get_actor_location())
                a=actor_1.get_actor_bounds(0)
                actor_1.set_actor_location((x,y,z+a[1].z),0,1)
                rdl= random.sample(range(-200, 200), 2) #rdl random_displacement_list 
                #random_height=random.sample(range(z+100, z+300), 1)
                point_light_coordinates=[x+rdl[0],y+rdl[1],350]#random_height[0]]
                pl=unreal.EditorLevelLibrary().spawn_actor_from_class(actor_class=unreal.PointLight, location=point_light_coordinates, rotation=[0.000000, 0.000000, 0.000000]) 
                random_light_colour=random.sample(range(100,255), 3)
                random_intensity=random.sample(range(0,8), 1)
                pl.point_light_component.set_editor_property("light_color",random_light_colour)
                pl.point_light_component.set_editor_property("intensity",random_intensity[0])
                if not mat_path==1:
                    temp_coordinates=[x,y,100]
                    actor_2=spawn_actor_by_object_path(mat_path,temp_coordinates)
                    actor_2.set_actor_scale3d((0.001,0.25,0.25))
                    #actor_2.get_editor_property("decal").set_editor_property("decal_size",(1024,2048,2048))
                    actor_2.set_actor_rotation(new_rotation=(270,0,90), teleport_physics=1)  
                if actor_count%100==0:
                    print(actor_count)
                # if actor_count>=100:
                    # exit()
                actor_count+=1
                if actor_count%50==0:
                    unreal.SystemLibrary().collect_garbage()

    print("Time taken to spawn" + str(actor_count)+" actors =")
    print("--- %s seconds ---" % (time.time() - start_time_actors))
    # Half the spacing on either side is required for the good spacing
    center_coordinates_for_ppvs,x_y_extent=sub_rectangles(lat_factor=2,long_factor=3,westlimit=x_min-spacing/2, southlimit=y_min-spacing/2, eastlimit=x_max+spacing/2, northlimit=y_max+spacing/2)
    #Create the post process volumes around subrectangles for each variation of saturation or contrast
    #z_floor=100.050232
    start_time_ppvs = time.time()
    print(center_coordinates_for_ppvs,x_y_extent)
    print("len(center_coordinates_for_ppvs) :",len(center_coordinates_for_ppvs))
    saturation_list=[0.5,1,2]
    contrast_list=[1,1.5]
    i=0
    #Create post process volumes based on the saturation and contrast settings
    for saturation_setting in saturation_list:
        for contrast_setting in contrast_list:
    # for i in range(len(center_coordinates_for_ppvs)):
            #getting x,y and z from a list of (x,y) tuples to determine the center of each ppv
            
            temp_coordinates=[center_coordinates_for_ppvs[i][0],center_coordinates_for_ppvs[i][1],100] 
            #First we get hieght and width of rectangles to apply them for the post process voumes 
            #x_y extent already taken from the subrectangles function and the height of the post process volume, z should be taken from the max height of the camera to be taken . Now hardcoded
            absolute_extent = [x_y_extent[1],x_y_extent[0], 1000]
            #ppvs have a default (200,200,200) extent and they need to be scaled accordingly
            post_process_scale = tuple([c/200 for c in absolute_extent])
            post_process_volume_list=unreal.EditorLevelLibrary().spawn_actor_from_class(actor_class=unreal.PostProcessVolume, location=temp_coordinates, rotation=[0.000000, 0.000000, 0.000000]) 
            post_process_volume_list.set_actor_scale3d(post_process_scale)  #Default 
            post_process_volume_list.settings.set_editor_property("override_color_saturation",True)
            #To test random saturation in each post post_process_volume creating a random list of [r,g,b,y]
            # saturaion_list = [round(random.uniform(0,2),2) for i in range(4)]
            # saturation_tuple=tuple(saturaion_list)
            post_process_volume_list.settings.set_editor_property("color_saturation",(1,1,1,saturation_setting)) #This worked 
            #Overriding colour contrast 
            post_process_volume_list.settings.set_editor_property("override_color_contrast",True)
            post_process_volume_list.settings.set_editor_property("color_contrast",(1,1,1,contrast_setting)) #This worked 
            i=i+1
    print("Time taken to spawn" + str(actor_count)+" post_process_volumes =")
    print("--- %s seconds ---" % (time.time() - start_time_ppvs))
    # start_time_floors = time.time()
    unreal.SystemLibrary().collect_garbage()
    #No floors so ignornig that section underneath

    # westlimit=x_min-spacing/2
    # southlimit=y_min-spacing/2
    # eastlimit=x_max+spacing/2
    # northlimit=y_max+spacing/2
    # #TOtally only 4 different types of materials. So only 2 x 2  floors in total 
    # latitude_factor=2 
    # longitude_factor=2
    # #Create floors to put them down
    # #Calcilate the coordinates first
    # center_coordinates_for_floors,x_y_extent_floors=sub_rectangles(lat_factor=latitude_factor,long_factor=longitude_factor,westlimit=x_min-spacing/2, southlimit=y_min-spacing/2, eastlimit=x_max+spacing/2, northlimit=y_max+spacing/2)
    # path_of_floors='/Game/Imports/NewImports'
    # floor_path_list=return_static_object_paths(path_of_floors)
    # for i in range(len(center_coordinates_for_floors)):
        # #getting x,y and z from a list of (x,y) tuples to determine the center of each ppv
        # temp_coordinates=[center_coordinates_for_floors[i][0],center_coordinates_for_floors[i][1],100.5] 
        # #First we get hieght awwwwwnd width of rectangles to apply them for the post process voumes 
        # #x_y extent already taken from the subrectangles function and the height of the post process volume, z sw
        # absolute_extent = [x_y_extent_floors[1],x_y_extent_floors[0], 100.5]
        # #ppvs have a default (200,200,200) extent and they need to be scaled accordingly
        # actor_1=spawn_actor_by_object_path(floor_path_list[i%len(floor_path_list)],temp_coordinates)
        # scale = tuple([c/400 for c in absolute_extent])
        # actor_1.set_actor_scale3d(scale)
        # # static_mesh =actor_1.static_mesh_component.static_mesh
    # print("Time taken to spawn" + str(len(center_coordinates_for_floors))+" floors =")
    # print("--- %s seconds ---" % (time.time() - start_time_floors))
    
    # print("TOtal time taken =, %s" % (time.time() -  start_time_actors))


# if __name__ == "__main__":
     # main(sys.argv[1:])
# #unreal.EditorAssetLibrary().list_assets(directory_path="/Game")