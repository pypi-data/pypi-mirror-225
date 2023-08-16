from mc.CompatibilityShims import BufferUtils
from mc import Resources
from pyglet import gl

class Textures:
    __idMap = {}

    @classmethod
    def loadTexture(cls, resourceName, mode):
        if resourceName in cls.__idMap:
            return cls.__idMap[resourceName]

        ib = BufferUtils.createUintBuffer(1)
        ib.clear()
        gl.glGenTextures(1, ib)
        id_ = ib.get(0)
        cls.__idMap[resourceName] = id_

        gl.glBindTexture(gl.GL_TEXTURE_2D, id_)

        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, mode)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, mode)

        img = Resources.textures[resourceName]
        w = img[0]
        h = img[1]

        pixels = BufferUtils.createIntBuffer(w * h << 2).clear()
        pixels.put(img[2], 0, len(img[2]))
        pixels.position(0).limit(len(img[2]))

        gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, w, h, 0, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, pixels)

        return id_
