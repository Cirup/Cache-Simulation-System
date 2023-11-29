# CSARCH2 Cache Simulation
## Cache System Specifications:
- Type: 8-Way Block Set Associative + Load Through
- Number of cache blocks = 16 blocks
- Cache line = 32 words
- Read policy: load-through
- Number of memory blocks = user input

## How the program works?
1. Input Number of Memory Blocks
2. Choose option for sequence of memory block - (Sequential, Random, Mid-Way Repeat)
3. Choose between by steps-by-step simulation or final snapshot
3. At the end, output will be displayed and final cache memory allocated

## Detail Test Case Analysis
Let us assume n = # of cache block = 16

### Sequential sequence
In a sequential sequence, we assume that reading of main memory sequence is in a consecutive block order and it will be repeated 4 times. 

Let us run through the sequence where: 
    n = 16
	number of sequence = 2(16) * 4 = 128 sequences
	The output it generates

![github-small](images\final_snapshot_sequential.jpg)
	

### Random sequence: containing 4n blocks.
### Mid-repeat blocks: Start at block 0, repeat the sequence in the middle two times up to n-1 blocks, after
which continue up to 2n. Then, repeat the sequence four times. Example: if n=8, sequence=0, 1,2,3,4,5,6,
1,2,3,4,5,6, 7,8,9,10,11,12,13,14,15 {4x}

Output:
* System output:
    * Cache memory snapshot.
        * Option for step-by-step animated tracing or final memory snapshot
        * Provide a text log of the cache memory trace (regardless of whether it is a step-by-step or final memory snapshot).
* Output: 1. memory access count; 2. cache hit count; 3. cache miss count; 4. cache hit rate; 5. cache miss rate; 6. average memory access time; 7. total memory access time
* Detail analysis of the three test cases. It will be submitted as “readme” to your GitHub. Note: Don’t forget to specify the full specs of your cache simulation system
* Video containing the “walkthrough” of your system. Specify the link, or it can be stored in GitHub.
* Note: the source code /executable program (stand-alone) or link to the web-based app, as well as the video
and analysis writeup, should all be in GitHub.
* Project demo if needed. Either face-to-face or through Zoom.