def x1_IOU(box1,box2):
    '''
    Calculate the overlap rate of the two boxes
    :param box: list like [x,y,w,h]
            (x,y):The upper-left coordinates of the box
            (w,h):The width and height of the box
    :return: Overlap rate :The ratio of intersection to union of two boxes
    '''
    I_x1 = max(box1[0],box2[0])
    I_y1 = max(box1[1],box2[1])
    I_x2 = min(box1[0]+box1[2],box2[0]+box2[2])
    I_y2 = min(box1[1]+box1[3],box2[1]+box2[3])
    if I_x1 > I_x2 or I_y1 > I_y2:
        return 0
    else:
        I_acre = (I_x2-I_x1)*(I_y2-I_y1)
        iou = I_acre/(box1[2]*box1[3]+box2[2]*box2[3]-I_acre)
        return iou
def max(num1,num2):
    '''
    Return a larger number
    '''
    if num1 > num2:
        return num1
    else:
        return num2
def min(num1,num2):
    '''
    Return a smaller number
    '''
    if num1 < num2:
        return num1
    else:
        return num2

if __name__ == '__main__':
    import random
    box1 = [1,1,9,9]
    box2 = [2,2,1,1]
    print(box1)
    print(box2)
    print(x1_IOU(box1,box2))