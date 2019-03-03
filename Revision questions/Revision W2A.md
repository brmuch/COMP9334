10. An interactive system has 50 terminals and the user's think time is equal to 5 seconds. The utilization of one of the system's disk was measured to be 60%. The average service time at the disk is equal to 30 msec. Each user interaction requires, on average, 4 I/Os on this disk. What is the average response time of the interactive system?

	**Answer:**
	

	    In this interactive system,  
	    	utilisation U = 60%
	    	interactive users M = 50
	    	mean thinking time Z = 5s
	    	mean service time per completed request S = 30 * 10^-3 / 4 = 7.5 * 10^-3s
	    so, according to Utilisation Law,
	    	output rate X = U / S = 8 requests per sec.
	    	
	    Next, according to the interactive response time law,
	    	the average response time of the interactive system R = M / X - Z = 50 / 8 - 5 = 1.25s
	    	
------
**Question 1.**  If the inter-arrival time of requests at a server is exponentially distributed wit a mean rate of 20 requests per second, answer the following questions.

 - a) What is the mean inter-arrival time?
 - b) Over a duration of 1 minute, what is the mean number of requests arriving at the server?
 - c) Over a duration of 1 minute, what is the probability of having no arrivals at the server?
 - d) Over a duration of 1 minute, what is the probability of having 10 arrivals at the server?

**Answer:**

    a) λ  = 20 requests per sec
    so the mean inter-arrival time t = 1 / 20 = 0.05s
    b) the mean number of requests arriving at the server in one minute is : 60 * 20 = 1200 requests
    c) following by Poission procss:
       Prob[no arrivals in 1 minutes] = (λt)^n * exp(-λt) / n! = (20 * 60) ^0 * exp(-20 * 60) / 0! = exp(-1200)
    d) same with c),
	   Prob[10 arrivals in 1 minutes] = (20 * 60)^10 * exp(-20*60) / 10! = 1200^10 * exp(-1200) / 10!
----
**Question 2.** This question is about Poisson Process. A server receives requests from two arrival processes. Both arrival processes at Poisson. The rates of these two processes are r1 and r2 respectively. Assume these two processes are independent prove that the aggregation of these two arrival processes is also Poisson. What is the aggregated arrival rate?

    arrival rate = r1 + r2

