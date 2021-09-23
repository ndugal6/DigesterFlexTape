# DigesterFlexTape - Nicholas Dugal
Take home for Gecko Robotics


# Interesting findings & Observations
* The y "feet" had negative values. Unsure how that would be represented in real life.
<br>If x "feet" had negative values, then y having possible negs would be understandable

* It's clear from a height of ~129 -> 224 inches that issues were had with getting measurements. I'm curious is figuring out why that is & how it could be resolved.
<br>This is problematic since the middle region appears to be needing the most repair work, therefore sparse data isn't ideal

*  Initially I figured something was wrong with my coding for areas that needed manual review,
 <br>but after looking at the volume of data that was marked as not considered valid, it made sense.
 <br> A highlight to this problem is that 325060 data points were invalid while only 185906 were valid!
 
 
* I was initially surprised by how well weak sections were masked by the heat map that used only base min thickness. 
<br>Although, since different locations have different allowable minimum thickness, a heatmap that doesn't take this into consideration is expected to be significantly less useful. 


* If I were working on this, I would stress the importance of accuracy in data for the more prone sections. 
There's massive cost associated with having invalid data, & having the "red" bordering the "white" squares in the simple heatmap should be alarming.
<br> I would further explore different step & batch sizes in the aggregation of data to see if it allows more things to come to life. 
<br> Finally, similar to how the mean of bottom 10 was useful, there's plenty of further derived data points that could provide insightful data &
 using a 3d model instead of 2d plots would let us learn more than a 1d color point for each location & reveal useful info.    

# 


### If you want to execute, you can run these commands:
`pip3 install -r requirements.txt`

`python3 index.py`
