class Solution {
    public int maxProfit(int[] prices) {
        int n = prices.length;
        int res = 0;
        int buy = Integer.MAX_VALUE;
        
        for(int i=0;i<n;i++){

            res = Math.max(res , prices[i] - buy);

            buy = Math.min(buy, prices[i]);


        }


        return res;


    }
}