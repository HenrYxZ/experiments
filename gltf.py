from pygltflib import GLTF2


def main():
    filename = "assets/Fox.glb"
    gltf = GLTF2().load(filename)
    print(gltf.accessors)


if __name__ == '__main__':
    main()
