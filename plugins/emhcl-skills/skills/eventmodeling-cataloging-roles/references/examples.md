# Role catalog example: a city bike rental

Use this example to compare the level of detail of your catalog.

## Human roles

Rider: a person who rents a bike for a trip.

- Key actions: reserve a bike, start a ride, end a ride, report a damaged bike.
- Cannot: change prices, move bikes between stations, give refunds.

Station Keeper: staff who look after the bikes at a group of stations.

- Key actions: take a bike out of service, put a bike back in service, move a bike to another station.
- Cannot: start a ride for a rider, change a rider account, give refunds.

Support Agent: staff who help riders with problems after a ride.

- Key actions: give a refund, close a damage report, block a rider account.
- Cannot: reserve bikes, change prices.

## System actors

Card Processor: outside this system.

- Acts when: this system asks it to charge a card.
- Contact: it sends a message back when the charge clears or fails.

Reservation Timer: inside this system.

- Acts when: a reservation reaches its end time without a ride start.
- Contact: it reacts to the passing of time and asks for the reservation to expire.

## Signs of a weak catalog

- An entry called "User" or "Admin user" with every action.
- Two roles with the same actions and limits, for example "Rider" and "Customer".
- A role with no limits. Each real role has things it cannot do.

## In an .em.hcl model

The Reservation Timer is inside the system. The roles part does not write it. It becomes a request concerning `processor`.

```hcl
actor "rider" {
  description   = "Rents a bike for a trip. Can reserve, start, and end a ride, and report damage. Cannot change prices, move bikes, or give refunds."
  auth_required = true
}

actor "station_keeper" {
  description   = "Looks after bikes at a group of stations. Can take a bike out of service and move it. Cannot start a ride or give refunds."
  auth_required = true
}

system "card_processor" {
  title       = "Card Processor"
  description = "Charges a card on request and reports when the charge clears or fails."
  external    = true
}

bounded_context "card_processing" {
  external = true
  owner    = system.card_processor
}

hotspot "reservation_timer_needed" {
  kind     = "request"
  concerns = "processor"
  question = "Add a Reservation Timer that reacts when a reservation reaches its end time without a ride start?"
}

evidence_source "rental_brief" {
  kind     = "document"
  location = "docs/rental-brief.pdf"
}

evidence "rider_from_brief" {
  certainty = "stated"
  source    = evidence_source.rental_brief
  location  = "section 1, page 2"
  on        = actor.rider
}
```
