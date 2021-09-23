# DigesterFlexTape - Nicholas Dugal
Take home for Gecko Robotics


# Interesting findings & Observations
* The y "feet" had negative values. I'm unsure how that would be represented in real life. 
If x "feet" had negative values, then y having possible negs would be understandable, but it has the expected min of 0.0.

* It's clear that from a height of ~129 -> 224 inches there issues with getting measurements. I'm curious as to why that is & how it could be resolved.
This is problematic since the middle region appears to be needing the most repair work, therefore sparse data isn't ideal.

*  I figured something was wrong with my coding for areas that needed manual review,
 but after looking at the volume of data that was marked as invalid, it made sense.
 A highlight to this problem is that 325060 data points were invalid while only 185906 were valid!
 
 
* I was initially surprised by how well weak sections were masked by the heat map that only the base min thickness. 
Although, since different locations have different allowable minimum thickness, a heatmap that doesn't take this into consideration is expected to be significantly less useful. 


* If I were working on this, I would stress the importance of accuracy in data for the more prone sections. 
There's massive cost associated with having invalid data, & having the "red" bordering the "white" squares in the simple heatmap should be alarming.
I would further explore different step & batch sizes in the aggregation of data to see if it allows more things to come to life. 
Similar to how the mean of bottom 10 was useful, there's plenty of further derived data points that could provide insights. &
Finally, using a 3d model instead of 2d plots would let us learn more than a 1d color point for each location & reveal useful info (ie: you can visualize the skew for a datapoint at each coordinate).    

* Going back to the start, I would've guessed that the top would be in most need for repair, instead of the middle. 
Although it has less a restrictive minimal thickness, I expected it would be more exposed to air & therefore corrosion.

### If you want to execute, you can run these commands:
`pip3 install -r requirements.txt`

`python3 index.py`
