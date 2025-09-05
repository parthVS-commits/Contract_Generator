# simple_promissory.py
template = """SIMPLE PROMISSORY NOTE
Date: {{insert_date}}
Place: {{insert_place}}

For value received, I, {{borrower_full_name}}, son/daughter of {{parents_name}},
residing at {{borrower_address}}, hereby unconditionally promise to pay to
{{lender_full_name}}, son/daughter of {{lender_parents_name}}, residing at
{{lender_address}}, the sum of {{amount_in_words}} ({{amount_in_figures}}) on or
before {{due_date}}.

The payment shall be made at {{lender_address_or_location}}, and I agree to pay the
said amount without any conditions or delay.

In case of failure to pay the above-mentioned sum on or before the due date, I agree to
pay an interest of {{interest_rate}}% per annum on the principal amount until the
payment is made in full.

This is a promissory note, and I affirm the obligation to repay the sum mentioned above
as per the terms set forth in this document.

Signed by Borrower:
{{borrower_full_name}}
{{borrower_signature}}

Witnesses:
Name: {{witness_1_name}}
Address: {{witness_1_address}}
Signature: __________________________

Name: {{witness_2_name}}
Address: {{witness_2_address}}
Signature: __________________________

NOTE:
Stamp Duty (as per Indian Stamp Act): Ensure the promissory note is properly stamped
according to the rates specified under the Indian Stamp Act, 1899, for promissory notes
in your state or region.
"""