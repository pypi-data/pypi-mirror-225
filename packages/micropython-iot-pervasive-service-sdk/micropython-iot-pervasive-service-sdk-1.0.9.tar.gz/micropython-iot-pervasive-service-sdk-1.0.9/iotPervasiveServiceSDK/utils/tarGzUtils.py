import gc
import uzlib
import upip_utarfile as tarfile
import upip
import os
import time

class TarGzUtils:
    def __init__(self, filename):
        # 检查文件名是否以.tar.gz结尾
        if not filename.endswith(".tar.gz"):
            raise ValueError("Invalid filename: {}".format(filename))
        self.filename = filename
    
    def extractToDir(self, dir):
        t1 = time.ticks_ms()
        # 清理内存
        gc.collect() 
        gzdict_sz = 16 + 15
        sz = gc.mem_free() + gc.mem_alloc()
        print('sz', sz)
        if sz <= 65536:
            gzdict_sz = 16 + 12
        # 解压.tar.gz文件到指定目录
        try:
          with open(self.filename, "rb") as f1:
            # 使用zlib模块创建一个解压对象
            f2 = uzlib.DecompIO(f1, gzdict_sz)
            # 使用tarfile模块打开解压后的文件对象
            f3 = tarfile.TarFile(fileobj=f2)
            # 提取所有文件到指定目录
            upip.install_tar(f3, dir)
        finally:
          del f3
          del f2
          gc.collect()
        t2 = time.ticks_ms()
        print(f"耗时：{t2-t1} ms")
    
    def extractAndDeleteToDir(self, dir):
        try :
            # 解压并删除.tar.gz文件到指定目录
            self.extractToDir(dir)
        finally :
            # 删除原始文件
            os.remove(self.filename) 
