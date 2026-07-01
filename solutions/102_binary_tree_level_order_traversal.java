/**
 * Definition for a binary tree node.
 * public class TreeNode {
 *     int val;
 *     TreeNode left;
 *     TreeNode right;
 *     TreeNode() {}
 *     TreeNode(int val) { this.val = val; }
 *     TreeNode(int val, TreeNode left, TreeNode right) {
 *         this.val = val;
 *         this.left = left;
 *         this.right = right;
 *     }
 * }
 */
class Solution {
    public List<List<Integer>> levelOrder(TreeNode root) {
        List<List<Integer>> res = new ArrayList<>();

        ArrayList<TreeNode> q = new ArrayList<>();


        q.add(root);


        while(q.size()!=0){

            int n = q.size();
            ArrayList<Integer> lst = new ArrayList<>();

            for(int i=0;i<n;i++){

            TreeNode temp = q.get(0);
            q.remove(0);
            if(temp!=null){
                if(temp.left!=null){
                    q.add(temp.left);    
                }
                if(temp.right!=null){
                    q.add(temp.right);    
                }
            lst.add(temp.val);
            }


            }
            
            if(lst.size()!=0){
                res.add(lst);
            }



        }


        return res;



    }
}