import bpy
import math
from mathutils import Vector

class OBJECT_PT_cartesian_product_panel(bpy.types.Panel):
    bl_label = "Cartesian Product"
    bl_idname = "OBJECT_PT_cartesian_product"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tool'

    def draw(self, context):
        layout = self.layout

        obj = context.selected_objects

        row = layout.row()
        row.label(text="Generate Cartesian Product:")

        row = layout.row()
        row.operator("object.generate_cartesian_product", text="Generate")

class OBJECT_OT_generate_cartesian_product(bpy.types.Operator):
    bl_idname = "object.generate_cartesian_product"
    bl_label = "Generate Cartesian Product"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Your script code here
        selected_obj = context.selected_objects
        selected_meshes = [obj for obj in selected_obj if obj.type == 'MESH']

        if selected_obj[0] is not None and selected_obj[0].type == 'MESH':
            mesh = selected_obj[0].data
            connected_vertex_tuples_array = self.get_connected_vertices(mesh)

            for vertex_tuple in connected_vertex_tuples_array:
                vertex1 = Vector(vertex_tuple[0].co)
                vertex2 = Vector(vertex_tuple[1].co)
                self.duplicate_and_rotate_meshes(selected_obj[1], [vertex1, vertex2])

        return {'FINISHED'}

    def get_connected_vertices(self, mesh):
            # Check if the input is a valid mesh
        if mesh is None or not isinstance(mesh, bpy.types.Mesh):
          print("Error: Input must be a valid mesh.")
          return []

    # Create an array to store connected vertex tuples
        connected_vertex_tuples = []

    # Iterate through the edges
        for edge in mesh.edges:
           vertex1 = mesh.vertices[edge.vertices[0]]
           vertex2 = mesh.vertices[edge.vertices[1]]
           vertex_tuple = (vertex1, vertex2)
           connected_vertex_tuples.append(vertex_tuple)

        return connected_vertex_tuples


    def duplicate_and_rotate_meshes(self, selected_obj, vertex_positions):
        duplicated_objects = []

    # Duplicate the selected object
        duplicate_obj1 = selected_obj.copy()
        duplicate_obj2 = selected_obj.copy()

    # Link duplicated objects to the collection
        bpy.context.collection.objects.link(duplicate_obj1)
        bpy.context.collection.objects.link(duplicate_obj2)

    # Set new locations for the duplicated objects
        duplicate_obj1.location = vertex_positions[0]
        duplicate_obj2.location = vertex_positions[1]

    # Calculate the direction vector between the two vertices
        direction_vector = vertex_positions[1] - vertex_positions[0]

    # Calculate the rotation angle around the Z-axis to align with the direction
        r = math.sqrt(direction_vector.x**2 + direction_vector.y**2 + direction_vector.z**2)
        phi = math.atan2(direction_vector.y, direction_vector.x)
        theta = math.acos(direction_vector.z / r)

    # Apply the rotation to the duplicated objects
        duplicate_obj1.rotation_euler = (0, theta, phi)
        duplicate_obj2.rotation_euler = (0, theta, phi)

    # Update the scene to apply changes
        bpy.context.view_layer.update()

        duplicated_objects.append(duplicate_obj1)
        duplicated_objects.append(duplicate_obj2)

        return duplicated_objects

def register():
    bpy.utils.register_class(OBJECT_PT_cartesian_product_panel)
    bpy.utils.register_class(OBJECT_OT_generate_cartesian_product)

def unregister():
    bpy.utils.unregister_class(OBJECT_PT_cartesian_product_panel)
    bpy.utils.unregister_class(OBJECT_OT_generate_cartesian_product)

if __name__ == "__main__":
    register()
