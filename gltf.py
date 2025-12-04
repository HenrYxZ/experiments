from pygltflib import GLTF2, Accessor, Skin, Node


def main():
    filename = "assets/Fox.glb"
    gltf = GLTF2().load(filename)
    current_scene = gltf.scenes[gltf.scene]
    node_index = current_scene.nodes[0]
    fox = gltf.nodes[node_index]
    m = fox.matrix  # will output vertices for the box object
    print(gltf.accessors)


if __name__ == '__main__':
    main()
