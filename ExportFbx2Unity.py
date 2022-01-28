from math import pi
import bpy
bl_info = {
    # required
    'name': 'Export FBX to Unity',
    'blender': (2, 93, 0),
    'category': 'Object',
    # optional
    'version': (1, 0, 0),
    'author': 'weijianjie',
    'description': 'A quickly export fbx to unity plugin',
}

# == GLOBAL VARIABLES
PROPS = [
    # ('importPath', bpy.props.StringProperty(name='ImportPath', default='')),
    ('exportPath', bpy.props.StringProperty(name='ExportPath', default='')),
    ('fbxName', bpy.props.StringProperty(name='FBX Name', default='')),
    # ('autoSave', bpy.props.BoolProperty(name='Auto Save', default=False)),
]

AutoSave = False
currentExportPath = ""


class ExportFBXPanel(bpy.types.Panel):
    bl_idname = 'VIEW3D_PT_example_panel'
    bl_label = 'Export Fbx to Unity'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    def draw(self, context):
        col = self.layout.column()
        for(prop_name, _) in PROPS:
            row = col.row()
            row.prop(context.scene, prop_name)
        col.operator('opr.export_operator', text='Export')
        # global AutoSave
        # AutoSave = context.scene.autoSave
        # print(AutoSave)


class ExportFBXOperator(bpy.types.Operator):
    bl_idname = 'opr.export_operator'
    bl_label = 'Object Export'
    bl_description = 'Export to Unity : )'

    def execute(self, context):
        global currentExportPath
        currentExportPath = context.scene.exportPath
        print(currentExportPath)
        currentExportPath = currentExportPath + '\\' + context.scene.fbxName
        if not currentExportPath.endswith(".fbx"):
            currentExportPath += ".fbx"

        # sCollection = bpy.context.collection
        for sCollection in bpy.data.collections:
            root = bpy.data.objects.new("empty", None)
            # bpy.context.collection.objects.link(root)
            bpy.context.scene.collection.objects.link(root)
            # sCollection.objects.link(bpy.context.collection)
            root.name = sCollection.name
            parentCol(sCollection, root)

        # item = 'EMPTY'
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.select_by_type(type='MESH')
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='SELECT')

        # for obj in bpy.context.visible_objects:
        for obj in bpy.data.objects:
            if obj.type == 'OBJECT':
                obj.location = (-obj.location.x, -
                                obj.location.y, obj.location.z)
                obj.rotation_euler.z += pi
            if obj.type == 'EMPTY':
                obj.rotation_euler.z += pi

        bpy.ops.export_scene.fbx(
            filepath=currentExportPath,
            use_selection=True,
            axis_forward='Z', axis_up='Y',
            apply_scale_options='FBX_SCALE_UNITS',
            object_types={'MESH', 'EMPTY'},
            use_space_transform=True,
            bake_space_transform=True,)

        # for obj in bpy.context.visible_objects:
        for obj in bpy.data.objects:
            if obj.type == 'OBJECT':
                obj.location = (-obj.location.x, -
                                obj.location.y, obj.location.z)
                obj.rotation_euler.z -= pi
                if abs(obj.rotation_euler.z * pi - 0.001) < 0.01:
                    obj.rotation_euler.z = 0
                # obj.rotation_euler = (0.0, 0.0, 0.0)
        bpy.ops.object.select_all(action='DESELECT')

        # item = 'EMPTY'
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.select_by_type(type='EMPTY')
        bpy.ops.object.delete()

        # ExportFBX(bpy.context.visible_objects)
        self.report({'INFO'}, "Export Successfully")
        return {'FINISHED'}

    # def AutoSaveOperator():
    #     print("Save")
    #     if AutoSave:
    #         if len(currentExportPath) != 0:
    #             print(len(currentExportPath))
    #             ExportFBX(bpy.context.visible_objects)
    #             print("Save")
    #     return 5.0


def parentCol(_colParent, _objParent):
    for col in _colParent.objects:
        print(col.name)
        col.parent = _objParent
        # newObj = bpy.data.objects.new("empty", None)
        # bpy.context.scene.collection.objects.link(newObj)
        # newObj.name = col.name
        # newObj.parent = _objParent
        # if len(col.objects) > 0:
        #     objs = col.objects
        #     for obj in objs:
        #         obj.parent = _objParent
        # else:
        #     parentCol(col, _objParent)


# def ExportFBX(objs):
#     if currentExportPath == "":
#         return

#     for obj in objs:
#         obj.location = (-obj.location.x, -obj.location.y, obj.location.z)

#     bpy.ops.export_scene.fbx(
#         filepath=currentExportPath,
#         axis_forward='Z', axis_up='Y',
#         apply_scale_options='FBX_SCALE_UNITS',
#         object_types={'MESH'},
#         use_space_transform=True,
#         bake_space_transform=True,)

#     for obj in objs:
#         obj.location = (-obj.location.x, -obj.location.y, obj.location.z)


MODULES = [
    ExportFBXPanel,
    ExportFBXOperator,
    # AutoSaveOperator,
]


def register():
    print('registered')  # just for debug
    # bpy.app.timers.register(ExportFBXOperator.AutoSaveOperator)

    for (prop_name, prop_value) in PROPS:
        setattr(bpy.types.Scene, prop_name, prop_value)

    for mod in MODULES:
        bpy.utils.register_class(mod)


def unregister():
    # print('unregistered')  # just for debug
    # bpy.app.timers.unregister(ExportFBXOperator.AutoSaveOperator)

    for (prop_name, _) in PROPS:
        delattr(bpy.types.Scene, prop_name)

    for mod in MODULES:
        bpy.utils.unregister_class(mod)


if __name__ == '__main__':
    register()
