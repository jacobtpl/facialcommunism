# Facial Communism

## Inspiration

Can you relate to looking back at your group photos and feeling slightly jealous? Feeling like everyone in there looked so much better than you? Traditionally, most approaches to tackling this problem involve applying some kind of beautify filter. But why beautify yourself when you can drag everyone down with you? 

The 19th-century visionary Karl Marx said, _"From each according to his ability, to each according to his needs."_ And when it comes to looks, what could be better than when the entire group works together so everyone can look great?
 
With **_Facial Communism_**, we accept that beauty doesn’t stem from being more attractive than others, rather, it’s about being the least ugly. **And when everyone is equally ugly, then everyone is beautiful.**

## What it does

**_Facial Communism_** replaces the faces of everyone in the photo with the same averaged face. No one will ever outshine you in a group photo again!

## How we built it

We harnessed Python OpenCV's capabilities to identify the number of faces, as well as dlib to identify 68 key landmark points of each face. By performing a Delaunay triangulation, each face could be mapped to any other face via affine transforms of the constituent triangles. Each face was replaced by the pixel average of all the faces (under the affine transforms) via alpha blending, and the facial borders were smoothly blended with the frame of the face. In this way, everyone in the photo would appear to have an identical face, but with slight variations in facial orientation (corresponding to the orientation before processing). Even in communism, not everyone is perfectly equal!

Next, we created and deployed **_Facial Communism_** as a webapp onto a website. This was done by linking a python Flask backend to process the user-uploaded pictures at our HTML/CSS frontend.

## Challenges we ran into

We found tremendous difficulty in linking up the backend python processing files with HTML frontend. We also struggled with extracting and sending the webcam video image to be processed, which was a feature we intended to incorporate. Smoothing the edges of each face was also a big challenge, as we had to do so without degrading the quality of the rest of the face.

## Accomplishments that we're proud of

In 24 hours, we managed to develop a reliable and effective facial blending software that blends multiple faces together as desired. In addition to incorporating several different libraries for facial detection, we designed our own new, efficient algorithm for smooth blending of the edges of the faces, to ensure that the blended faces fit well into the new image while maintaining the quality of the face.

## What we learned

We should have figured out the backend-frontend link before embarking on both. We should also have come up with an idea beforehand, as we spent way too long on ideation and had insufficient time for development.

## What's next for **_Facial Communism_**?

The website could be improved. Oops. Also, to take photos directly from the webcam. And a button to download the blended photos! We hope to extend **_Facial Communism_** to work in real-time video as well - imagine how cool that would be!
