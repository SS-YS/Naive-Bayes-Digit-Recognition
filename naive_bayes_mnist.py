import random

THRESHOLD = 100
CPT = {i: {n: {"above_threshold": 0, "below_threshold": 0} for n in range(10)} for i in range(784)}

def normalize(d):
    totalValue = sum(d.values())
    for key in d:
        d[key] = d[key] / totalValue
    return d

def train():
    data = [list(map(int, line.strip().split(","))) for line in open("mnist_train.csv").read().strip().split("\n")]
    
    for i in range(len(data)):
        row = data[i]
        label = row[0]
        pixels = row[1:]

        for num_pixel in range(784):
            pixel = pixels[num_pixel]
            if pixel > THRESHOLD:
                CPT[num_pixel][label]["above_threshold"] += 1
            else:
                CPT[num_pixel][label]["below_threshold"] += 1

    for i in range(784):
        for n in range(10):
            CPT[i][n] = normalize(CPT[i][n])

# data: 1D array of 28*28=784 grayscale pixels. Each pixel ranges from 0-255. 
def predict(data):
    # P(C|x1, ..., x784) = normalize P(x1|C) * ... * P(x784|C) 
    highest_prob, highest_num = -9999, None
    for num in range(10):
        cur_prob = 1
        for num_pixel in range(784):
            pixel = data[num_pixel]
            if pixel > THRESHOLD:
                cur_prob *= CPT[num_pixel][num]["above_threshold"]
            else:
                cur_prob *= CPT[num_pixel][num]["below_threshold"]
        if cur_prob >= highest_prob:
            highest_prob = cur_prob
            highest_num = num
    return highest_num

def convert_1d_2d(arr1d, col=28):
    result = []
    for start in range(0, len(arr1d), col):
        result.append(arr1d[start:start+col])
    return result

def show_image(pixels):
    pixels = convert_1d_2d(pixels)
    ASCII = " .:-=+*#%@"
    MAGIC = 256//len(ASCII)+1
    art = "\n".join(["".join([ASCII[item//MAGIC] for item in row]) for row in pixels])
    print(art)

def run_test(auto=True, no_graphics=False):
    data = [list(map(int, line.strip().split(","))) for line in open("mnist_test.csv").read().strip().split("\n")]
    correct = 0
    for i in range(len(data)):
        row = data[i]
        label = row[0]
        pixels = row[1:]
        prediction = predict(pixels)

        if label == prediction:
            correct += 1

        print("No.{}\nPredict: {}\nActual: {}\nAccumulative precision: {}".format(i+1, prediction, label, correct/(i+1)))
        if not no_graphics: show_image(pixels)
        if not auto: input("Press enter to continue.")

if __name__=="__main__":
    train()
    run_test()
