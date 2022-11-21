def main(inputs, outputs, parameters, synchronise):
    auto_enable = True
    try:
        enable = inputs.read_number("Enable")
    except Exception:
        auto_enable = True

    

    while(auto_enable or inputs.read_number('Enable')):
        bbox = inputs.read_array("BoundingBox")
        pcl2 = inputs.read_array("PointCloud")
        if bbox is None or pcl2 is None:
            continue

        x = int(bbox[0]+bbox[2]/2)
        y = int(bbox[1]+bbox[3]/2)

        pcl_point = (x+640*y)*4+2
        dist = pcl2[pcl_point]
        
        print("DISTANCIA -> " + str(dist))
        outputs.share_number("Linear", dist)






