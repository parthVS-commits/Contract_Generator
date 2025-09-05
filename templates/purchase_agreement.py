# purchase_agreement.py
template = """PURCHASE AGREEMENT
This Purchase Agreement ("Agreement") is made and entered into on this
{{date_of_execution}}, by and between:
1. {{seller_name}}, with its principal office located at {{seller_address}} (hereinafter
referred to as the "Seller" or "we"),
and
2. {{buyer_name}}, with its principal office located at {{buyer_address}} (hereinafter
referred to as the "Buyer" or "you").
WHEREAS, the Seller agrees to sell, and the Buyer agrees to purchase, the product(s)
described below under the terms and conditions set forth in this Agreement;
NOW, THEREFORE, in consideration of the mutual promises, covenants, and
undertakings herein contained, the parties agree as follows:
1. Sale of Goods
The Seller agrees to sell, and the Buyer agrees to purchase, the following product(s)
("Product(s)"):
- {{product_description}}
The Product(s) will be delivered by the Seller to the Buyer under the terms and
conditions set forth in this Agreement. The Seller guarantees that the Product(s) sold
hereunder shall be free from any liens or encumbrances and shall conform to the
specifications provided by the Seller in the product listing, marketing materials, or other
agreed documents.
2. Purchase Price
The total purchase price for the Product(s) is {{purchase_price}}, payable by the Buyer
in the following manner:
- {{payment_terms}}
The total purchase price does not include taxes, duties, or additional fees imposed by
government authorities, which shall be borne by the Buyer unless otherwise agreed in
writing.
3. Payment Terms
The Buyer agrees to pay the Seller the total purchase price of {{purchase_price}}.
Payment will be made in accordance with the following schedule:
{{payment_terms}}
The Buyer agrees to make timely payment for the Product(s) upon receipt of the invoice
from the Seller. Late payments will incur a penalty of {{late_payment_penalty}} per
month on the outstanding amount.
4. Delivery of Products
The Seller shall deliver the Product(s) to the Buyer according to the following terms:
- {{delivery_terms}}
The risk of loss or damage to the Product(s) passes to the Buyer upon delivery unless
otherwise agreed upon. Delivery shall be made at the Buyer's designated address or
another agreed-upon location. The Buyer shall be responsible for shipping, handling,
and insurance costs unless otherwise agreed.
5. Inspection Rights
Upon receipt of the Product(s), the Buyer has the right to inspect the Product(s) within
[insert number] days of delivery. The Buyer must notify the Seller in writing of any
defects, discrepancies, or damages identified during the inspection. If no such notice is
received within the inspection period, the Product(s) shall be deemed accepted.
6. Warranty
The Seller warrants that the Product(s) are free from defects in material and
workmanship for a period of {{insert_warranty_period}} e.g., 12 months from the date of
delivery. If any Product(s) are found to be defective within this period, the Seller agrees
to repair or replace the Product(s) at no additional charge to the Buyer, subject to the
following conditions:
- The Buyer notifies the Seller of any defects within {{no_of_days}} days of discovering
the issue.
- The defective Product(s) are returned to the Seller at the Buyer's expense, unless
otherwise agreed.
7. Title and Risk of Loss
Title to the Product(s) shall transfer to the Buyer upon full payment of the purchase
price. The risk of loss or damage to the Product(s) passes to the Buyer upon delivery,
unless otherwise agreed. The Buyer assumes all responsibility for the Product(s) upon
delivery.
8. Limitation of Liability
The liability of the Seller under this Agreement shall be limited to the total purchase
price paid by the Buyer for the specific Product(s) that gave rise to the claim. In no
event shall the Seller be liable for any indirect, incidental, consequential, or punitive
damages arising from the sale or use of the Product(s), even if the Seller has been
advised of the possibility of such damages.
9. Force Majeure
Neither party shall be liable for failure to perform its obligations under this Agreement
due to any event beyond its reasonable control, including but not limited to, acts of God,
natural disasters, war, civil unrest, strikes, or government restrictions ("Force Majeure").
In the event of a Force Majeure, the affected party shall notify the other party as soon
as reasonably possible of the occurrence of such an event.
10. Termination
This Agreement may be terminated by either party under the following conditions:
- By mutual written consent of both parties.
- By the Buyer if the Product(s) do not conform to the specifications or warranties
provided in this Agreement.
- If either party breaches any material provision of this Agreement and fails to remedy
such breach within [insert number of days] after receiving written notice from the
non-breaching party.
- Upon the occurrence of a Force Majeure Event.
Upon termination, the Buyer agrees to pay for all Product(s) delivered up to the date of
termination, and the Seller agrees to return any property or confidential information
belonging to the Buyer.
11. Dispute Resolution
In the event of any dispute arising out of or in connection with this Agreement, the
parties agree to first attempt to resolve the dispute through amicable negotiation. If the
dispute cannot be resolved through negotiation, the parties agree to submit to
{{dispute_resolution_method}}, and the decision will be binding.
12. Governing Law
This Agreement shall be governed by and construed in accordance with the laws of
{{governing_law}}. Any dispute, claim, or legal action arising out of this Agreement shall
be subject to the exclusive jurisdiction of the courts located in {{jurisdiction}}, and the
parties hereby submit to the jurisdiction of such courts.
13. Miscellaneous
- Entire Agreement: This Agreement constitutes the entire understanding between the
parties and supersedes all prior agreements, whether oral or written, regarding the sale
of the Product(s).
- Amendments: This Agreement may only be amended or modified in writing, signed by
both parties.
- Severability: If any provision of this Agreement is found to be invalid or unenforceable
by a court of competent jurisdiction, the remaining provisions shall remain in full force
and effect.
IN WITNESS WHEREOF, the parties hereto have executed this Purchase Agreement
as of the date first written above.
For the Seller:
Signature: __________________________
Name: {{seller_name}}
Designation: {{seller_designation}}
Date: {{date_of_execution}}
For the Buyer:
Signature: __________________________
Name: {{buyer_name}}
Designation: {{buyer_designation}}
Date: {{date_of_execution}}
"""