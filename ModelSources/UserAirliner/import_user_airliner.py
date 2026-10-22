import bpy
from pathlib import Path
from mathutils import Vector
root=Path('/Users/aimee/Documents/Codex/2026-10-11/x20-r')
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.wm.obj_import(filepath='/Users/aimee/Downloads/3d-model.obj')
objects=[o for o in bpy.context.scene.objects if o.type=='MESH']
points=[o.matrix_world@Vector(v) for o in objects for v in o.bound_box];lo=Vector(tuple(min(v[i] for v in points) for i in range(3)));hi=Vector(tuple(max(v[i] for v in points) for i in range(3)));center=(lo+hi)/2;scale=63/(hi.y-lo.y)
mat=bpy.data.materials.new('Plain airliner finish');mat.diffuse_color=(.78,.82,.86,1);mat.use_nodes=True;bs=mat.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(.78,.82,.86,1);bs.inputs['Roughness'].default_value=.35
for obj in objects:
 obj.name='User airliner airframe'
 world=obj.matrix_world.copy()
 for v in obj.data.vertices:v.co=(world@v.co-center)*scale
 obj.matrix_world.identity();obj.data.materials.clear();obj.data.materials.append(mat)
 for poly in obj.data.polygons:poly.material_index=0
out=root/'work/user-airliner';out.mkdir(exist_ok=True)
bpy.ops.export_scene.fbx(filepath=str(out/'UserAirliner.fbx'),use_selection=False,object_types={'MESH'},axis_forward='-Z',axis_up='Y',bake_space_transform=True,add_leaf_bones=False)
print('Exported 63m airliner, original OBJ axes preserved for catalog YawOffset=180')
