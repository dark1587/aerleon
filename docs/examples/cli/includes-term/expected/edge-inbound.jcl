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
            /*
             ** Deny reserved ranges.
             */
            term deny-reserved {
                from {
                    source-address {
                        0.0.0.0/8;
                        240.0.0.0/4;
                    }
                }
                then {
                    discard;
                }
            }
            /*
             ** Deny bogon ranges.
             */
            term deny-bogons {
                from {
                    source-address {
                        192.0.0.0/24;
                        192.0.2.0/24;
                    }
                }
                then {
                    discard;
                }
            }
            term default-deny {
                then {
                    discard;
                }
            }
        }
    }
}
