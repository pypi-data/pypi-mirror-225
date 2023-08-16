import tqdm
from multiprocessing import Pool

def fun(params):
    (pic_dir, image_name) = params
    return image_name

images_name_list = [1,2,3]
param_list = [('zhusitao',image_name) for image_name in images_name_list]
with Pool(16) as p:
    r = list(tqdm.tqdm(p.imap(fun, param_list), total=len(param_list), desc='多进程旋转图片：'))
p.close()
p.join()
r = list(set(r))
print('r=',r)
#r.remove(None)  # 删除无效返回值

