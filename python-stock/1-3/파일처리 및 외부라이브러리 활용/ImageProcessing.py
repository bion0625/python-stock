import matplotlib.pyplot as plt
import matplotlib.image as mpimg

dst_img = mpimg.imread('dst.png')

print(dst_img)

pseudo_img = dst_img [:,:,0] # 1

print(pseudo_img)

plt.suptitle('image Processing', fontsize=18)

plt.subplot(1,2,1) # 1
plt.title('Original Image')
plt.imshow(mpimg.imread('src.png'))

plt.subplot(122) # 2
plt.title('Pseudocolor Image')
dst_img = mpimg.imread('dst.png')
pseudo_img = dst_img[:,:,0]
plt.imshow(pseudo_img)

plt.show()