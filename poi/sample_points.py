# -*- coding:utf-8 -*-
# 2024.10.15
'''
输入shp文件：打断相交线
此程序实现，
1. 计算道路长度
2. 标记道路等级
3. 合并双线道路
4. 删除复杂短街道
5. 删除悬挂街道
6. 生成简化道路
7. 计算道路方向角
8. 沿线生成采样点（固定间隔和中点采样）
9. 转换采样点坐标系并计算经纬度
10. 删减字段，保留ID、方向角和经纬度
11. 导出属性表为CSV文件
'''
import os
import arcpy
import math
import sys

if __name__ == "__main__":
    # Set environment settings
    # 工作环境设置
    arcpy.env.workspace = sys.path[0]  # 设置环境为当前脚本运行目录
    arcpy.env.overwriteOutput = True

    # 输入文件路径
    InputShp = r"F:\pythonProject\WUY\WUY.shp"  # 输入的原始打断相交线后的路网
    SingleShp = r"F:\pythonProject\WUY\ZANCUN\Single_WUY.shp"  # 处理后的单一shp文件
    MergeShp = r"F:\pythonProject\WUY\ZANCUN\Merge_WUY.shp"  # 合并双线后的shp文件
    ThinShp = r"F:\pythonProject\WUY\ZANCUN\Thin_WUY.shp"  # 删除短街道后的shp文件
    SimplifiedShp = r"F:\pythonProject\WUY\ZANCUN\Simplified_WUY.shp"  # 简化后的路网shp文件
    SamplePointsShp = r"F:\pythonProject\WUY\ZANCUN\sample_points_WUY.shp"  # 固定间隔采样点文件
    MidPointsShp = r"F:\pythonProject\WUY\ZANCUN\mid_points_WUY.shp"  # 中点采样点文件
    CombinedPointsShp = r"F:\pythonProject\WUY\ZANCUN\combined_points_WUY.shp"  # 合并的采样点文件
    CombinedPointsWGS84Shp = r"F:\pythonProject\WUY\OUTPUT\combined_points_wgs84_WUY.shp"  # 转换为WGS84的采样点文件
    CsvOutput = r"F:\pythonProject\WUY\OUTPUT\sample_points_WUY.csv"  # 导出的CSV文件路径

    # 1. 计算道路长度
    if 'length' not in [f.name for f in arcpy.ListFields(InputShp)]:
        arcpy.AddField_management(InputShp, "length", "DOUBLE")  # 新建长度字段
        print("Length field has been added.")


    arcpy.CalculateGeometryAttributes_management(InputShp, [["length", "LENGTH_GEODESIC"]], "METERS")
    print("Road lengths have been calculated.")

    # 2. 创建图层，标记道路等级
    field_names = [f.name for f in arcpy.ListFields(InputShp)]
    if "level" not in field_names:
        arcpy.AddField_management(InputShp, "level", "SHORT")
        print("Level field has been added.")

    arcpy.MakeFeatureLayer_management(InputShp, "RoadLayer")

    # 选择并标记 "高架及快速路"
    arcpy.SelectLayerByAttribute_management("RoadLayer", "NEW_SELECTION", "type = '高架及快速路'")
    selected_count = arcpy.GetCount_management("RoadLayer")
    print(f"Selected '高架及快速路' roads: {selected_count}")
    if int(selected_count[0]) > 0:  # 只有在有选中的道路时才赋值
        arcpy.CalculateField_management("RoadLayer", "level", 1)
    arcpy.SelectLayerByAttribute_management("RoadLayer", "CLEAR_SELECTION")

    # 选择并标记 "城市主干路"
    arcpy.SelectLayerByAttribute_management("RoadLayer", "NEW_SELECTION", "type = '城市主干路'")
    selected_count = arcpy.GetCount_management("RoadLayer")
    print(f"Selected '城市主干路' roads: {selected_count}")
    if int(selected_count[0]) > 0:  # 只有在有选中的道路时才赋值
        arcpy.CalculateField_management("RoadLayer", "level", 2)
    arcpy.SelectLayerByAttribute_management("RoadLayer", "CLEAR_SELECTION")

    # 选择并标记 "城市次干路"
    arcpy.SelectLayerByAttribute_management("RoadLayer", "NEW_SELECTION", "type = '城市次干路'")
    selected_count = arcpy.GetCount_management("RoadLayer")
    print(f"Selected '城市次干路' roads: {selected_count}")
    if int(selected_count[0]) > 0:  # 只有在有选中的道路时才赋值
        arcpy.CalculateField_management("RoadLayer", "level", 3)
    arcpy.SelectLayerByAttribute_management("RoadLayer", "CLEAR_SELECTION")

    # 选择并标记 "城市支路"
    arcpy.SelectLayerByAttribute_management("RoadLayer", "NEW_SELECTION", "type = '城市支路'")
    selected_count = arcpy.GetCount_management("RoadLayer")
    print(f"Selected '城市支路' roads: {selected_count}")
    if int(selected_count[0]) > 0:  # 只有在有选中的道路时才赋值
        arcpy.CalculateField_management("RoadLayer", "level", 4)
    arcpy.SelectLayerByAttribute_management("RoadLayer", "CLEAR_SELECTION")

    # 选择并标记 "郊区乡村道路" 或 "内部道路"
    arcpy.SelectLayerByAttribute_management("RoadLayer", "NEW_SELECTION", "type IN ('郊区乡村道路', '内部道路')")
    selected_count = arcpy.GetCount_management("RoadLayer")
    print(f"Selected '郊区乡村道路/内部道路' roads: {selected_count}")
    if int(selected_count[0]) > 0:  # 只有在有选中的道路时才赋值
        arcpy.CalculateField_management("RoadLayer", "level", 5)
    arcpy.SelectLayerByAttribute_management("RoadLayer", "CLEAR_SELECTION")

    # 选择并标记 "人行道路" 或 "自行车道"
    arcpy.SelectLayerByAttribute_management("RoadLayer", "NEW_SELECTION", "type IN ('人行道路', '自行车道')")
    selected_count = arcpy.GetCount_management("RoadLayer")
    print(f"Selected '人行道路/自行车道' roads: {selected_count}")
    if int(selected_count[0]) > 0:  # 只有在有选中的道路时才赋值
        arcpy.CalculateField_management("RoadLayer", "level", 6)
    arcpy.SelectLayerByAttribute_management("RoadLayer", "CLEAR_SELECTION")

    # 将处理后的图层保存为 SingleShp
    arcpy.CopyFeatures_management("RoadLayer", SingleShp)
    print(f"Processed road network has been saved to {SingleShp}.")

    # 3. 合并双线道路
    arcpy.MakeFeatureLayer_management(SingleShp, "Project_lyr")
    arcpy.MergeDividedRoads_cartography("Project_lyr", "level", "30 meters", MergeShp)
    print("The double-line road is merged.")

    # 4. 删除复杂短街道
    arcpy.AddField_management(MergeShp, "visibility", "SHORT")
    print("AddField_management is done.")
    arcpy.CalculateField_management(MergeShp, "visibility", 0)
    print("CalculateField_management is done.")
    arcpy.MakeFeatureLayer_management(MergeShp, "Thin_lyr")
    print("MakeFeatureLayer_management is done.")
    arcpy.SelectLayerByAttribute_management("Thin_lyr", "NEW_SELECTION", '"visibility" = 0')
    print("SelectLayerManagement is done.")
    arcpy.CopyFeatures_management("Thin_lyr", ThinShp)
    print("The complex streets are deleted.")

    # 5. 删除悬挂街道
    arcpy.TrimLine_edit(ThinShp, "10 meters", "DELETE_SHORT")
    print("The dangle streets are deleted.")

    # 6. 生成简化道路并投影
    out_coordinate_system = arcpy.SpatialReference(3857)
    arcpy.Project_management(ThinShp, SimplifiedShp, out_coordinate_system)
    print("Simplified road network has been projected to WGS_1984_Web_Mercator_Auxiliary_Sphere.")

    # 7. 计算道路方向角
    arcpy.AddGeometryAttributes_management(SimplifiedShp, "LINE_BEARING")
    print("The road bearings (direction angles) have been calculated.")

    # 8. 沿线生成采样点
    interval = 150  # 自定义间距，单位为米

    # 8.1 创建图层并选择长度在120米到200米之间的道路
    arcpy.MakeFeatureLayer_management(SimplifiedShp, "MediumRoads", '"length" > 120 AND "length" < 200')
    arcpy.FeatureVerticesToPoints_management("MediumRoads", MidPointsShp, "MID")
    print("Mid-points have been generated for roads with length between 120 and 200 meters.")

    # 8.2 对长度大于等于200米的道路生成固定间隔采样点
    arcpy.MakeFeatureLayer_management(SimplifiedShp, "LongRoads", '"length" >= 200')
    arcpy.GeneratePointsAlongLines_management("LongRoads", SamplePointsShp, 'DISTANCE',
                                              Distance=str(interval) + ' Meters')
    print(f"Sample points have been generated along roads longer than or equal to {interval} meters.")

    # 8.3 合并固定间隔点和中点
    arcpy.management.Merge([SamplePointsShp, MidPointsShp], CombinedPointsShp)
    print("Combined sample points with mid-points and interval points have been created.")

    # 8. 沿线生成采样点 (采用35-45m的固定间距，这里选择40m)
    # interval = 40  # 这里设置采样的固定间隔距离为40米
    #
    # 8.1 对所有道路进行固定间隔采样
    # arcpy.GeneratePointsAlongLines_management(SimplifiedShp, SamplePointsShp, 'DISTANCE',
    #                                           Distance=str(interval) + ' Meters')
    # print(f"Sample points have been generated along all roads with a fixed interval of {interval} meters.")

    # 9. 转换采样点坐标系并计算经纬度
    wgs84 = arcpy.SpatialReference(4326)
    arcpy.Project_management(CombinedPointsShp, CombinedPointsWGS84Shp, wgs84)
    print("Sample points have been projected to WGS84 geographic coordinate system.")
    arcpy.AddGeometryAttributes_management(CombinedPointsWGS84Shp, "POINT_X_Y_Z_M")
    print("The longitude and latitude of each sample point have been calculated.")

    # 10. 删减字段，保留ID、方向角和经纬度
    fields_to_keep = ["FID", "BEARING", "POINT_X", "POINT_Y"]
    all_fields = [f.name for f in arcpy.ListFields(CombinedPointsWGS84Shp) if
                  f.name not in fields_to_keep and f.type != "Geometry"]

    if all_fields:
        arcpy.DeleteField_management(CombinedPointsWGS84Shp, all_fields)
        print(f"Fields {all_fields} have been deleted, only ID, direction angle, longitude, and latitude are kept.")
    else:
        print("No fields need to be deleted.")

    # 11. 导出属性表为CSV文件
    arcpy.TableToTable_conversion(CombinedPointsWGS84Shp, os.path.dirname(CsvOutput), os.path.basename(CsvOutput))
    print(f"The attribute table has been exported to {CsvOutput}.")
