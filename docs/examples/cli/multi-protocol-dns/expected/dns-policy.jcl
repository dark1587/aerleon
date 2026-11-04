firewall {
    family inet {
        /*
         ** $Id:$
         ** $Date:$
         ** $Revision:$
         **
         */
        replace: filter dns-both {
            interface-specific;
            /*
             ** Allow DNS over both UDP and TCP.
             */
            term allow-dns {
                from {
                    destination-address {
                        10.0.0.53/32;
                    }
                    protocol [ tcp udp ];
                    destination-port 53;
                }
                then accept;
            }
        }
    }
}
firewall {
    family inet {
        /*
         ** $Id:$
         ** $Date:$
         ** $Revision:$
         **
         */
        replace: filter dns-udp-only {
            interface-specific;
            /*
             ** Listing only udp silently drops TCP 53.
             */
            term allow-dns-udp {
                from {
                    destination-address {
                        10.0.0.53/32;
                    }
                    protocol udp;
                    destination-port 53;
                }
                then accept;
            }
        }
    }
}
