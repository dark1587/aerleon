firewall {
    family inet {
        /*
         ** $Id:$
         ** $Date:$
         ** $Revision:$
         **
         */
        replace: filter edge-inbound {
            interface-specific;
            /*
             ** Allow SSH from the management network.
             */
            term allow-ssh {
                from {
                    source-address {
                        10.0.0.0/24;
                        192.168.10.0/24;
                    }
                    protocol tcp;
                    destination-port 22;
                }
                then accept;
            }
            term default-deny {
                then {
                    discard;
                }
            }
        }
    }
}
