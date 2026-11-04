firewall {
    family inet {
        /*
         ** $Id:$
         ** $Date:$
         ** $Revision:$
         **
         */
        replace: filter gre-https {
            interface-specific;
            /*
             ** GRE has no ports, so it gets its own term.
             */
            term allow-gre {
                from {
                    destination-address {
                        192.0.2.1/32;
                    }
                    protocol gre;
                }
                then accept;
            }
            /*
             ** HTTPS to the same peer.
             */
            term allow-https {
                from {
                    destination-address {
                        192.0.2.1/32;
                    }
                    protocol tcp;
                    destination-port 443;
                }
                then accept;
            }
        }
    }
}
