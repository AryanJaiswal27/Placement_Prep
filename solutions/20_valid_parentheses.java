class Solution {
    public boolean isValid(String s) {
        int n = s.length();
        
        ArrayDeque<Character> stk = new ArrayDeque<>();

        for(int i=0;i<n;i++){

            if((s.charAt(i)=='{')||(s.charAt(i)=='(')||(s.charAt(i)=='[')){
                if(s.charAt(i)=='{'){
                stk.offerLast('}');

                }
                else if (s.charAt(i)=='('){

                stk.offerLast(')');

                }
                else{

                stk.offerLast(']');
                }


            }
            else{

                if(stk.size()==0)
                    return false;

                if(stk.peekLast() == s.charAt(i)){

                    stk.pollLast();

                }
                else{
                    return false;
                }

            }



        }

        if(stk.size()==0)
            return true;

        return false;
    }
}