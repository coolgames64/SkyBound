import bpy,math,json
from pathlib import Path
from mathutils import Vector,Matrix
root=Path('/Users/aimee/Documents/Codex/2026-10-11/x20-r');bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.wm.obj_import(filepath='/Users/aimee/Downloads/737+Max-8.obj',use_split_groups=True)
objects=[o for o in bpy.context.scene.objects if o.type=='MESH'];pts=[o.matrix_world@Vector(p) for o in objects for p in o.bound_box];lo=Vector(tuple(min(v[i] for v in pts) for i in range(3)));hi=Vector(tuple(max(v[i] for v in pts) for i in range(3)));center=(lo+hi)/2;scale=39.52/(hi.x-lo.x);rot=Matrix.Rotation(-math.pi/2,3,'Z')
def mat(name,color):
 m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True;b=m.node_tree.nodes.get('Principled BSDF');b.inputs['Base Color'].default_value=(*color,1);b.inputs['Roughness'].default_value=.36;return m
white=mat('Neutral fuselage',(.78,.82,.86));dark=mat('Dark metal',(.07,.08,.09));glass=mat('Cockpit glazing',(.055,.10,.13))
for o in objects:
 world=o.matrix_world.copy()
 for v in o.data.vertices:v.co=rot@((world@v.co-center)*scale)
 o.matrix_world.identity();o.data.materials.clear();o.data.materials.append(dark if 'gear' in o.name.lower() or 'blades' in o.name.lower() or 'black' in o.name.lower() else glass if 'wiper' in o.name.lower() else white)
 for p in o.data.polygons:p.material_index=0
 if 'gear' in o.name.lower():o.name='LandingGear_'+o.name
 if o.name.lower().startswith('blades'):
  for side,sign in [('Left',-1),('Right',1)]:
   faces=[list(p.vertices) for p in o.data.polygons if ((sum(o.data.vertices[v].co.x for v in p.vertices)/len(p.vertices)<0)==(sign<0))];indices=sorted(set(v for p in faces for v in p));mapping={v:i for i,v in enumerate(indices)}
   if not faces:continue
   m=bpy.data.meshes.new('EngineFan_'+side);m.from_pydata([o.data.vertices[v].co.copy() for v in indices],[],[[mapping[v] for v in p] for p in faces]);m.materials.append(dark);new=bpy.data.objects.new('EngineFan_'+side,m);bpy.context.collection.objects.link(new)
  bpy.data.objects.remove(o,do_unlink=True)
out=root/'work/user-737';out.mkdir(exist_ok=True)
bpy.ops.export_scene.fbx(filepath=str(out/'User737Max8.fbx'),use_selection=False,object_types={'MESH'},axis_forward='-Z',axis_up='Y',bake_space_transform=True,add_leaf_bones=False)
print('Exported 39.52m 737 MAX 8 with separate fan rotors and named landing gear')
