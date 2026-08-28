# Transport

Transport answers how an exact admitted object graph becomes a usable local tree without changing its identity.

Preferred reversible transports are:

1. already-present sibling checkout;
2. exact-SHA archive/materialization;
3. clone/fetch to exact SHA;
4. workflow artifact carrying the exact tree;
5. dependency-closed reconstruction when full history is unnecessary.

`ecosystem.lock.toml` defines the first bootstrap closure and sibling layout. Transport failure changes topology; it does not revoke the existence of other lawful transports.

A repository connector object is never treated as a mounted checkout. A checkout at the wrong SHA is never treated as the locked subject.
