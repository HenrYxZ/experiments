from pygltflib import GLTF2
import struct


def main():
    filename = "assets/Fox.glb"
    gltf = GLTF2().load(filename)
    current_scene = gltf.scenes[gltf.scene]
    node_index = current_scene.nodes[1]
    fox = gltf.nodes[node_index]
    # get the first mesh in the current scene (in this example there is only one scene and one mesh)
    mesh = gltf.meshes[fox.mesh]

    # get the vertices for each primitive in the mesh (in this example there is only one)
    for primitive in mesh.primitives:

        # get the binary data for this mesh primitive from the buffer
        accessor = gltf.accessors[primitive.attributes.POSITION]
        bufferView = gltf.bufferViews[accessor.bufferView]
        buffer = gltf.buffers[bufferView.buffer]
        data = gltf.get_data_from_buffer_uri(buffer.uri)

        # pull each vertex from the binary buffer and convert it into a tuple of python floats
        vertices = []
        for i in range(accessor.count):
            index = bufferView.byteOffset + accessor.byteOffset + i * 12  # the location in the buffer of this vertex
            d = data[index:index + 12]  # the vertex data
            v = struct.unpack("<fff", d)  # convert from base64 to three floats
            vertices.append(v)
        print(len(vertices))
        print(vertices[0])


if __name__ == '__main__':
    main()
