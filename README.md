[Stochastic Optimisation Report.md](https://github.com/user-attachments/files/31288586/Stochastic.Optimisation.Report.md)
## **Stochastic Optimisation of Traffic Signal Phasing via Spatial Occupancy Filtering** 

**By Aaron Aguele** 

# **1 Introduction** 

### **1.1 The Engineering behind Traffic Signal Optimisation** 

Traffic signal phasing is a critical mechanism in modern urban infrastructure, engineered to mitigate congestion, minimise total vehicle emissions and reduce human delays experienced as a result of commuting. Foundational traffic flow theory, most notably Webster's delay model (Webster, 1958), approached intersection design through deterministic frameworks. Contrastingly, modern traffic engineering recognises that the mechanics of vehicular arrival and departure are inherently stochastic. The Highway Capacity Manual (TRB, 2016), asserts that variables such as saturation headway ( ℎ ), which represents the time interval between consecutive vehicles discharging from a queue, fluctuate significantly due to driver reaction times and vehicle heterogeneity. Consequently, optimising traffic signal phases requires probabilistic modelling rather than static analytical solutions. 

### **1.2 Telemetry and Computer Vision** 

Historically, traffic arrival rates ( _μi_ ) were acquired through embedded inductive loop detectors, which suffer from spatial limitations and high maintenance costs. The advent of video-derived telemetry and Convolutional Neural Networks (CNNs) has revolutionised empirical data extraction, reducing these inefficiencies, without compromising data integrity (Buch et al., 2011). Real time object detection algorithms, specifically the YOLO (You Only Look Once) architecture (Redmon et al., 2016), allow for high-fidelity spatial extraction of vehicular flow. However, transforming frame-based occupancy from video footage into pure arrival rates required rigorous algorithmic filtering to prevent temporal aliasing and overdispersion, to ensure that the desired data is successfully extracted and the data conforms to theoretical probability distributions. 

### **1.3 Problem Definition and Objectives** 

This project investigates the computational optimisation of a four-armed intersection, wherein the West arm operates strictly as an exit-only flow. The primary objective is to design a signal phase model that minimises a non-linear wait-time penalty function ( _ωi_ ) for each arm of the intersection. 

4 The optimisation is strictly bound by a maximum cycle constraint of ∑(𝑅 + 𝐺 ) ≤600 seconds. 𝑖 𝑖 𝑖=1 The saturation headway is not a fixed scalar but rather a uniformly distributed random variable ( ℎ∼𝑈1. 8, 2. 2[ ] ), thus the objective function cannot be solved analytically. Instead, it necessitates a stochastic computational algorithm. 

In order to establish a mathematically robust cycle design, this study employs a methodology to multiple consecutive stages with the following objectives: 

- Empirical Data Extraction: Utilise YOLOv8 and Spatial Max-Occupancy filtering on traffic telemetry to extract accurate, de-duplicated arrival rates ( _μi_ ) for each intersection arm. 

- Stochastic Validation: Validate the randomness of the traffic flow by establishing equidispersion ( _μ_ ≈ _σ_<sup>2</sup> ) and fitting the empirical data to a theoretical Poisson Probability Mass Function. 

- Algorithmic Optimisation: Formulate a computational solution using Sequential Least Squares Programming (SLSQP) to minimise the total intersection wait time (Σ _ωi_ ). 

- Probabilistic Modelling **:** Execute 10,000 iterations of Monte Carlo simulations to account for headway uncertainty, establishing probabilistic confidence intervals for the optimal green light durations ( _Gi_ ). 

# **2 Methodology** 

This study details the implementation of a four stage pipeline, bridging empirical data extraction, statistical validation, mathematical optimisation, and stochastic simulation to produce a comprehensive traffic signal model within the Python 3 programming environment. 

### **2.1 Empirical Data Acquisition and Spatial Max-Occupancy Filtering** 

The foundational requirement of the model was to extract deterministic arrival rates ( _μi_ ) from aerial video telemetry. To counteract temporal aliasing, where slow-moving vehicles are redundantly counted across consecutive frames, a Spatial Maximum-Occupancy algorithm was engineered using the OpenCV (cv2) library. Thin "Detection Zones" (50-pixel depth) were computationally defined perpendicular to the traffic flow; this was paired with a YOLOv8 Convolutional Neural Network (ultralytics library) which evaluated the intersection telemetry at its native frequency (30 Hz). To translate this high-frequency spatial data into discrete temporal arrival rates, a maximum function was applied over every frame collectively, within 1-second bins. By extracting the maximum occupancy of the zone per second, the algorithm mathematically eliminated duplicate counts without relying on fragile ID-tracking algorithms, generating de-duplicated arrival frequencies. 

### **2.2 Statistical Validation using Poisson Distribution** 

Traffic arrivals are examples of discrete stochastic events. To validate the extracted data for the wait-time model, it was tested against the Poisson Probability Mass Function: 



For a dataset to be rigorously defined as a Poisson process, it must exhibit equidispersion, wherein the variance ( _σ_<sup>2</sup> ) is approximately equal to the mean ( _μ_ ). The extracted telemetry data was statistically evaluated using the libraries NumPy and Pandas to confirm this condition ( _μ_ ≈ _σ_<sup>2</sup> ). This step scientifically justified the use of the empirical mean as the primary arrival parameter for the numerical optimiser. 

### **2.3 Formulation of the Optimisation Model** 

The model's objective required minimising the intersection's non-linear wait-time penalty function (Σ _ωi_ ). A critical algebraic evaluation of the assignment's operational constraint, Σ(Ri + Gi) ≤ 600, revealed its underlying physical limitation. The red time for any lane equals the total cycle time minus its own green time (Ri = C - Gi) hence, summing this relation across four intersection arms yields 4C ≤ 600. Thus, the intersection is intrinsically bounded by a realistic 150-second maximum green time per arm. To solve this computationally, Sequential Least Squares Programming (SLSQP **)** was deployed via Python’s scipy.optimize library. SLSQP was specifically selected as it is mathematically designed to minimise non-linear objective functions subject to strict linear inequality constraints and boundary conditions (e.g. establishing a 0-second minimum for the exit-only West arm). 

### **2.4 Stochastic Simulation Framework** 

Deterministic optimisation is invalid when underlying variables are uncertain. Saturation headway ( _h_ ), which fluctuates for each vehicle, is modelled here as a uniform random variable 



<!-- Start of picture text -->
Arrival Distribution: North Arrival Distribution: East<br>0.6<br>[5 Actual Data 0.7 [5 Actual Data<br>—@ Poisson (u=0.55, o?=0.51) —@ Poisson (u=0.36, o?=0.37)<br>0.5 0.6<br>* \ °°<br>2 Zo.<br>& =© 03<br>0.2<br>0.2<br>0.1 \ 0.1 ™<br>|__—~~<br>0.0 0.0<br>-0.5 0.0 0.5 1.0 15 2.0 2.5 3.0 3.5 -0.5 0.0 0.5 1.0 15 2.0 2.5<br>Cars per Second Cars per Second<br>Arrival Distribution: South Arrival Distribution: West<br>(5 Actual Data 1.0 Actual Data<br>—@ Poisson (u=0.09, o?=0.08) —@ Poisson (u=0.00, o7=0.00<br>0.8<br>0.8<br>0.6<br>FSaoO £06aoO<br>Bos E<br>0.4<br>0.2 0.2<br>0.0 0.0<br>-0.50 -0.25 0.00 0.25 0.50 0.75 1.00 1.25 1.50 -0.4 -0.2 0.0 0.2 0.4<br>Cars per Second Cars per Second<br><!-- End of picture text -->



<!-- Start of picture text -->
Optimal Green Time Distribuiton: North Optimal Green Time Distribuiton: East Optimal Green Time Distribuiton: South<br>3500 3500<br>3000 3000 8000<br>S 2500 S 2500 Ss<br>So Ss 4<br>s s S 6000<br>‘S 2000 ‘S 2000 6<br>3s225 25<br>eo=zSg15001000 eo=zg5  15001000 <zovg3 4000<br>2000<br>500 500<br>0 0 0<br>10 15 20 25 30 6 8 10 12 14 16 18 20 5.0 5.1 5.2 5.3 5.4 5.5 5.6 5.7<br>Green Time (s) Green Time (s) Green Time (s)<br><!-- End of picture text -->

prediction covariance matrix. When the underlying Intersection-over-Union (IoU) spatial matching failed, the algorithm lost the temporal linkage and consequently, it terminated the original ID and generated a new ID for the exact same vehicle upon re-detection, artificially compounding the traffic count significantly. 

Recognising that attempting to iteratively tune the tracker's parameters to compensate for this spatial instability was a mathematically ineffective approach, the data extraction paradigm was entirely re-engineered. By engineering the Spatial Maximum-Occupancy function, the model bypassed the need for temporal state estimation entirely. This curiosity-driven pivot not only secured optimal empirical data but demonstrated that rigorous engineering often requires discarding overly complex and vulnerable algorithms in favour of mathematically stable solutions. 

# **4 Concluding Remarks** 

This study successfully engineered a stochastic traffic phase design by bridging computer vision telemetry with constrained numerical optimisation. By filtering temporal aliasing from empirical data and computationally navigating the uncertainty of saturation headways through stochastic analysis, the model proves that optimal intersection design requires dynamic probabilistic solutions rather than static deterministic formulas. The resulting model mathematically minimises the non-linear wait penalty while strictly adhering to physical safety constraints. 

# **References** 

Buch, N., Velastin, S. A., & Orwell, J. (2011) 'A review of computer vision techniques for the analysis of urban traffic', _IEEE Transactions on Intelligent Transportation Systems_ , 12(3), pp. 920-939. 

Redmon, J., Divvala, S., Girshick, R., & Farhadi, A. (2016) 'You only look once: Unified, real-time object detection', in _Proceedings of the IEEE conference on computer vision and pattern recognition_ (pp. 779-788). 

Transportation Research Board (TRB) (2016) _Highway Capacity Manual: A Guide for Multimodal Mobility Analysis_ . 6th edn. Washington, D.C.: National Academies of Sciences, Engineering, and Medicine. 

Webster, F. V. (1958) _Traffic Signal Settings_ . Road Research Technical Paper No. 39. London: Her Majesty’s Stationery Office. 

