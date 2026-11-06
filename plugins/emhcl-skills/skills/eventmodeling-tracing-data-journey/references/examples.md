# Example of a data journey

The model in this example describes a city bike service. The person asks: "Where does the rider phone number come from, and where does it go?"

The name search finds the fields phone, riderPhone, newPhone, and phoneVerified. The declared origins add contactNumber and smsRecipient, because these fields take their value from riderPhone and newPhone. The field phoneVerified only sounds similar. It holds a yes or no answer, not a phone number, so it is not a stop.

## The result

Rider phone number: starts in 2 places, stored in 2 events, transformed in 1 place, used in 2 places, sent in 1 place.

Summary: The rider phone number is marked as personal data. It enters at sign-up and at a phone change, and the text message service receives it for unlock codes. Gap: the support screen Rider Lookup shows a phone number, but no read model carries it to that screen.

| Role | Element | Field | Slice | Note |
| --- | --- | --- | --- | --- |
| origin | Sign Up Screen | phone | Sign Up Rider | The rider types it in. |
| used | Sign Up Rider | phone | Sign Up Rider | Must be unique for each rider. |
| stored | Rider Signed Up | riderPhone | Sign Up Rider | The event also holds phoneVerified, which is different information. |
| origin | Change Phone Number | newPhone | Change Phone Number | The screen for this change is not modeled, so the command is the start. |
| stored | Phone Number Changed | newPhone | Change Phone Number | Replaces the earlier number. |
| transformed | Rider Contact | contactNumber | Rider Contact | Takes the latest number and writes it in international format, as a scenario states. |
| used | Rider Profile Screen | contactNumber | Rider Contact | Shown to the rider. |
| sent | Send Unlock Code | smsRecipient | Send Unlock Code | Goes to the text message service. |

## Why the example looks like this

- The command Change Phone Number is an origin, because no screen for the change exists in the model.
- Rider Lookup is not a stop. No declared origin reaches it, so it appears only as a gap in the summary.
- The note of Rider Signed Up names phoneVerified, so the reader knows that the trace saw the field and left it out on purpose.
