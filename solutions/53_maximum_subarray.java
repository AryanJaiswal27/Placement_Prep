class Solution {
    public int maxSubArray(int[] nums) {
        
        int sum = Integer.MIN_VALUE;
        int n = nums.length;
        int curr = 0;
        for(int i=0;i<n;i++){
            
            
            
            if(curr<0){
                curr = nums[i];

            }
            else{

                curr += nums[i];

            }
            sum =  Math.max(curr,sum);
        }

        return sum;

    }
}