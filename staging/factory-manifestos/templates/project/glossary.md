<!--
Template note. Delete this comment when you copy the file into a project.

Replace the heading and the description. Replace the example term (Invoice) with the
project's first real term.

Each term has exactly one _Schema_ line, saying where the term lives:
- Low-code profile: the Dataverse table and column, flow or app.
  _Schema_: Dataverse table `getai_order`, column `getai_status`; flow `Order approval`
- Pro-code profile: the code symbol.
  _Schema_: class `Invoice` in `src/billing/invoice.ts`
- No home yet: _Schema_: none yet
Never put behaviour on the _Schema_ line.

Definitions are one or two sentences: what the term IS, not what it does. Only terms
specific to this project. Pick one word per concept and list the others under _Avoid_.
Group terms under subheadings when clusters emerge.
-->
# {Context Name}

{One or two sentence description of what this context is and why it exists.}

## Language

**Invoice**:
A request for payment sent to a customer after delivery.
_Schema_: Dataverse table `getai_invoice`
_Avoid_: Bill, payment request
