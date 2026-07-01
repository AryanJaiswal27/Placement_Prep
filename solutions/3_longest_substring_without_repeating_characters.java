class Solution {
    public int lengthOfLongestSubstring(String s) {
        int n = s.length();

        int l = 0;
        int r = 0;
        int res = 0;
        HashMap<Character, Integer> set = new HashMap<>();

        while(r<n){

            while(set.containsKey( s.charAt(r)) && l<r){
                if(set.get(s.charAt(l)) == 1){
                    set.remove(s.charAt(l));
                }else{
                    set.put( s.charAt(l) , set.get(s.charAt(l))-1 );

                }
                l++;
            }

            set.put( s.charAt(r), 1);
            res = Math.max( res , r-l+1);

            // System.out.println( "l: "+ l +", r: "+ r );

            r++;
        }

        return res;

    }
}