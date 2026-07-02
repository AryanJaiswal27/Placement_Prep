/**
 * Definition for singly-linked list.
 * public class ListNode {
 *     int val;
 *     ListNode next;
 *     ListNode() {}
 *     ListNode(int val) { this.val = val; }
 *     ListNode(int val, ListNode next) { this.val = val; this.next = next; }
 * }
 */
class Solution {
    public ListNode reverseList(ListNode head) {
        ListNode prev = null;
        ListNode next;
        ListNode temp;

        while(head!=null){
            
            next = head.next;
            temp = head;
            head.next = prev;
            head = next;
            prev = temp;


        }


        return prev; 

    }
}