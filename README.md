# SimilarClothes

#### Description:
- The aim of this project is to create an application with the primary objective of proficiently detecting visually similar clothing items.
- The application will be intricately linked to a comprehensive database housing a diverse collection of clothing from various stores.
- Users will be able to upload images of specific clothing item. In response, the application will provide a detailed list of similar clothes, inclusive of images, corresponding prices, and the names of stores where these similar items can be found.
- Demo: Our video
  
---

### Table of Contents
1. [How we did it?](#How-we-did-it?)
2. [Classification Model](#Classification-Model)
3. [Similarity Detection Model](#Similarity-Detection-Model)
4. [How to Install](#how-to-install)

---

## How we did it?
Our project mainly consists of two things:
1. Classification Model which classifies the different types of clothes. We have specifically narrowed our focus to four primary classes: jeans, jackets, shoes, and shirts. Leveraging the efficiency of YOLO (You Only Look Once), this model adeptly categorizes input images into one of these classes.
2. Similarity Detection Model which identifies clothing items with visual similarities to a specific input. We used the Siamese network, a specialized architecture designed for similarity learning. By utilizing this network, we enable the system to discern analogous clothing items based on visual features.
- The workflow seamlessly integrates both models to deliver a comprehensive solution. Once the Classification Model determines the clothing type of an input image, the system seamlessly transitions to the Similarity Detection Model. This latter model then conducts a search within the corresponding directory of that clothing type in the database, identifying and presenting visually similar items, inclusive of images, corresponding prices, and the names of stores where these similar items can be found.

---
  
## Classification Model




## Similarity Detection Model
- We used the Siamese network, a specialized neural network architecture designed for tasks involving similarity and distance measurement. Siamese networks are particularly useful in scenarios where the focus is on discerning the similarity or dissimilarity between pairs of input samples.
    - Paper Link: https://www.cs.cmu.edu/~rsalakhu/papers/oneshot1.pdf
- For training the network, it is fed pairs of examples, with one being a positive pair (similar image) and the other a negative pair (dissimilar image). During training, the network adjusts its weights through backpropagation to maximize the similarity between similar images and minimize the similarity between dissimilar images.

### Data collection for training siamese network
