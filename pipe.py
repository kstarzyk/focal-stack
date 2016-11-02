from PIL import Image
from scipy import signal as sg
import numpy as np
import os.path
import argparse

# GLOBALS
# set destination path of all results
DEST = './results/'

def read_img(name):
  return np.asarray(Image.open(name), dtype=np.float32)

def save_img(ar, name):
  Image.fromarray(ar.round().astype(np.uint8)).save(DEST + name)

def normalize(arr):
  return 255.*np.absolute(arr)/np.max(arr)

def intersect(a1, a2):
  (r1, c1) = a1.shape
  (r2, c2) = a2.shape
  return (a1[r1-r2 if r1>r2 else 0:,
    c1-c2 if c1>c2 else 0:],
    a2[r2-r1 if r2>r1 else 0::,
      c2-c1 if c2>c1 else 0:])

def gradient(im):
  ver, hor = intersect(sg.convolve(im, [[1., -1.]]), sg.convolve(im, [[1.], [-1.]]))
  return np.sqrt(np.power(ver, 2)+np.power(hor, 2)), ver, hor

def pipe(img, name):
  print("Generating partials...")
  name = name + '.png'
  grad_img, ver_img, hor_img = gradient(img)
  save_img(ver_img, 'ver_' + name)
  save_img(hor_img, 'hor_' + name)
  save_img(grad_img, 'gradient_' + name)
  print("Saved vertical edges: ver_" + name )
  print("Saved horizontal edges: hor_" + name )
  print("Saved gradient: gradient_" + name )
  return grad_img

def maxer(A,B,C, imgA, imgB, imgC):
  gradient_result = np.empty_like(A)
  result = np.empty_like(A)
  false_color = np.empty((len(imgA), len(imgA[0]), 3), dtype=np.uint8)
  for i in range(len(A)):
    for j in range(len(A[0])):
      max_value = max(A[i,j], B[i,j], C[i,j])
      gradient_result[i,j] = max_value
      if max_value == A[i,j]:
        result[i,j] = imgA[i,j]
        false_color[i,j] = [max_value,0,0]
      elif max_value == B[i,j]:
        result[i,j] = imgB[i,j]
        false_color[i,j] = [0,max_value,0]
      else:
        result[i,j] = imgC[i,j]
        false_color[i,j] = [0,0,max_value]

  save_img(false_color, 'contrib.png')
  print ("Saved: false colors as contrib.png")
  save_img(gradient_result, 'gradient_result.png')
  print ("Saved: gradient_result.png")
  return result


def main():
  print("Start")
  print("All the results file are inside results dir")
  a,b,c = read_img('./resources/stack1.png'), read_img('./resources/stack2.png'), read_img('./resources/stack3.png')
  ga,gb,gc = pipe(a, 'stack1'),pipe(b, 'stack2'),pipe(c, 'stack3')
  result = maxer(ga,gb,gc,a,b,c)
  save_img(result, 'result.png')
  print("Result saved to result.png")

if __name__ == "__main__":
  main()

