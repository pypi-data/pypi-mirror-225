from pyrfuniverse.envs.base_env import RFUniverseBaseEnv
import pyrfuniverse.attributes as attr
import cv2
import numpy as np

env = RFUniverseBaseEnv(assets=['Camera', 'GameObject_Box'])

camera = env.InstanceObject(name='Camera', id=123456, attr_type=attr.CameraAttr)
box = env.InstanceObject(name='GameObject_Box', attr_type=attr.GameObjectAttr)
box.SetTransform(position=[0, 0.05, 0.5], scale=[0.1, 0.1, 0.1])
box.SetColor([1, 0, 0, 1])
env.step()
camera.SetTransform(position=[0, 0.25, 0], rotation=[30, 0, 0])
camera.LookAt(target=box.data['position'])
camera.GetDepth(width=512, height=512, zero_dis=1, one_dis=5)
camera.GetDepthEXR(width=512, height=512)
camera.GetRGB(width=512, height=512)
env.step()
print(camera.data['depth'])
print(camera.data['depth_exr'])
print(camera.data['rgb'])
image = np.frombuffer(camera.data['rgb'], dtype=np.uint8)
image = cv2.imdecode(image, cv2.IMREAD_COLOR)
print(image.shape)
env.close()
cv2.imshow("rgb", image)
cv2.waitKey(0)
