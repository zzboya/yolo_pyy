import matplotlib.pyplot as plt
import numpy as np

classes1 = ['sugarcane','weed','background FP']
classes2 = ['sugarcane','weed','background FN']
confusion_matrix = np.array([(0.82,0.13,0.45),(0.11,0.79,0.55),(0.07,0.08, 0),],dtype=np.float64)
#confusion_matrix = np.array([(0.88,0.09,0.51),(0.06,0.86,0.49),(0.06,0.05, 0),],dtype=np.float64)
plt.figure(figsize=(8, 6))
plt.imshow(confusion_matrix, cmap=plt.cm.Blues)
#plt.title("Confusion Matrix")
tick_marks = np.arange(3)
plt.xticks(tick_marks, classes1,fontsize=14)
# plt.ylim(-0.2, 2.5)
plt.yticks(tick_marks, classes2, rotation=90,fontsize=14)

# yl = plt.gca().get_yaxis().get_label()
# yl.set_y(yl.get_position()[1] + 2)
#plt.subplots_adjust(left=0.15)

# Remove outer borders
ax = plt.gca()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)
plt.rcParams['font.size'] = 16
# Remove colorbar border
colorbar = plt.colorbar()
colorbar.outline.set_visible(False)

# Remove ticks and tick labels

plt.tick_params(axis='both', which='both', length=0)

# Add text annotations
thresh = confusion_matrix.max() / 2.
for i in range(confusion_matrix.shape[0]):
    for j in range(confusion_matrix.shape[1]):
        plt.text(j, i, format(confusion_matrix[i, j]),
                 ha="center", va="center",family="Times New Roman",
                 color="white" if confusion_matrix[i, j] > thresh else "black")

# Adjust the location of the y-axis labels


plt.ylabel('Predicted',fontproperties='Times New Roman')
plt.xlabel('True',fontproperties='Times New Roman')

# plt.subplots_adjust(left=0.2, right=0.9, top=0.9, bottom=0.1)
fig = plt.gcf()
#plt.show()
fig.savefig('confusion/confusion_matrix7.png', dpi=600)

