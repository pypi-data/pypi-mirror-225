import csv


from .classes import Node, Link, Network, Agent, ColumnVec, VDFPeriod, \
                     AgentType, DemandPeriod, Assignment, UI


__all__ = [
    'read_network',
    'output_columns',
    'output_link_performance'
 ]


def read_nodes(input_dir,
               nodes,
               id_to_no_dict,
               no_to_id_dict,
               zone_to_node_dict):

    """ step 1: read input_node """
    with open(input_dir+'/node.csv', 'r', encoding='utf-8') as fp:
        print('read node.csv')

        reader = csv.DictReader(fp)
        node_seq_no = 0
        for line in reader:
            # set up node_id, which should be an integer
            node_id = line['node_id']
            if not node_id:
                continue
            node_id = int(node_id)

            # set up zone_id, which should be an integer
            zone_id = line['zone_id']
            if not zone_id:
                zone_id = -1
            else:
                zone_id = int(zone_id)

            # treat them as string
            coord_x = line['x_coord']
            coord_y = line['y_coord']

            # construct node object
            node = Node(node_seq_no, node_id, zone_id, coord_x, coord_y)
            nodes.append(node)

            # set up mapping between node_seq_no and node_id
            id_to_no_dict[node_id] = node_seq_no
            no_to_id_dict[node_seq_no] = node_id

            # associate node_id to corresponding zone
            if zone_id not in zone_to_node_dict.keys():
                zone_to_node_dict[zone_id] = []
            zone_to_node_dict[zone_id].append(node_id)

            node_seq_no += 1

        print(f"the number of nodes is {node_seq_no}")


def read_links(input_dir,
              links,
              nodes,
              id_to_no_dict,
              agent_type_size,
              demand_period_size):

    """ step 2: read input_link """
    with open(input_dir+'/link.csv', 'r', encoding='utf-8') as fp:
        print('read link.csv')

        reader = csv.DictReader(fp)
        link_seq_no = 0
        for line in reader:
            # it can be an empty string
            link_id = line['link_id']

            # check the validility
            from_node_id = line['from_node_id']
            if not from_node_id:
                continue

            to_node_id = line['to_node_id']
            if not to_node_id:
                continue

            length = line['length']
            if not length:
                continue

            # pass validility check
            from_node_id = int(from_node_id)
            to_node_id = int(to_node_id)
            length = float(length)

            try:
                from_node_no = id_to_no_dict[from_node_id]
                to_node_no = id_to_no_dict[to_node_id]
            except KeyError:
                print(f"EXCEPTION: Node ID {from_node_no} "
                      f"or/and Node ID {to_node_id} NOT IN THE NETWORK!!")
                continue

            # for the following attributes,
            # if they are not None, convert them to the corresponding types
            # leave None's to the default constructor
            lanes = line['lanes']
            if lanes:
                lanes = int(lanes)

            link_type = line['link_type']
            if link_type:
                link_type = int(link_type)

            free_speed = line['free_speed']
            if free_speed:
                free_speed = int(free_speed)

            capacity = line['capacity']
            if capacity:
                # issue: int??
                capacity = int(float(capacity))

            # if link.csv does not have no column 'allowed_uses',
            # set allowed_uses to 'auto'
            try:
                allowed_uses = line['allowed_uses']
            except KeyError:
                allowed_uses = 'auto'

            # if link.csv does not have no column 'geometry',
            # set geometry to ''
            try:
                geometry = line['geometry']
            except KeyError:
                geometry = ''

            # construct link ojbect
            link = Link(link_id,
                        link_seq_no,
                        from_node_no,
                        to_node_no,
                        from_node_id,
                        to_node_id,
                        length,
                        lanes,
                        link_type,
                        free_speed,
                        capacity,
                        allowed_uses,
                        geometry,
                        agent_type_size,
                        demand_period_size)

            # VDF Attributes
            for i in range(demand_period_size):
                header_vdf_alpha = 'VDF_alpha' + str(i+1)
                header_vdf_beta = 'VDF_beta' + str(i+1)
                header_vdf_mu = 'VDF_mu' + str(i+1)
                header_vdf_fftt = 'VDF_fftt' + str(i+1)
                header_vdf_cap = 'VDF_cap' + str(i+1)
                header_vdf_phf = 'VDF_phf' + str(i+1)

                # case i: link.csv does not VDF attributes at all
                # case ii: link.csv only has partial VDF attributes
                # under case i, we will set up only one VDFPeriod ojbect using
                # default values
                # under case ii, we will set up some VDFPeriod ojbects up to
                # the number of complete set of VDF_alpha, VDF_beta, and VDF_mu
                try:
                    VDF_alpha = line[header_vdf_alpha]
                    if VDF_alpha:
                        VDF_alpha = float(VDF_alpha)
                except KeyError:
                    if i == 0:
                        # default value will be applied in the constructor
                        VDF_alpha = None
                    else:
                        break

                try:
                    VDF_beta = line[header_vdf_beta]
                    if VDF_beta:
                        VDF_beta = float(VDF_beta)
                except KeyError:
                    if i == 0:
                        # default value will be applied in the constructor
                        VDF_beta = None
                    else:
                        break

                try:
                    VDF_mu = line[header_vdf_mu]
                    if VDF_mu:
                        VDF_mu = float(VDF_mu)
                except KeyError:
                    if i == 0:
                        # default value will be applied in the constructor
                        VDF_mu = None
                    else:
                        break

                try:
                    VDF_fftt = line[header_vdf_fftt]
                    if VDF_fftt:
                        VDF_fftt = float(VDF_fftt)
                except KeyError:
                    # set it up using length and free_speed from link
                    VDF_fftt = length / max(0.001, free_speed) * 60

                try:
                    VDF_cap = line[header_vdf_cap]
                    if VDF_cap:
                        VDF_cap = float(VDF_cap)
                except KeyError:
                    # set it up using capacity from link
                    VDF_cap = capacity

                # not a mandatory column
                try:
                    VDF_phf = line[header_vdf_phf]
                    if VDF_phf:
                        VDF_phf = float(VDF_phf)
                except KeyError:
                    # default value will be applied in the constructor
                    VDF_phf = None

                # construct VDFPeriod object
                vdf = VDFPeriod(i, VDF_alpha, VDF_beta, VDF_mu,
                                VDF_fftt, VDF_cap, VDF_phf)

                link.vdfperiods.append(vdf)

            # set up outgoing links and incoming links
            nodes[from_node_no].add_outgoing_link(link)
            nodes[to_node_no].add_incoming_link(link)
            links.append(link)

            link_seq_no += 1

        print(f"the number of links is {link_seq_no}")


def read_demand(input_dir,
                file,
                agent_type_id,
                demand_period_id,
                zone_to_node_dict,
                demands,
                column_pool):

    """ step 3:read input_agent """
    with open(input_dir+'/'+file, 'r', encoding='utf-8') as fp:
        print('read demand.csv')

        at = agent_type_id
        dp = demand_period_id

        reader = csv.DictReader(fp)
        total_agents = 0
        for line in reader:
            volume = line['volume']

            # invalid origin zone id, discard it
            oz_id = line['o_zone_id']
            if not oz_id:
                continue

            # invalid destinationzone id, discard it
            dz_id = line['d_zone_id']
            if not dz_id:
                continue

            oz_id = int(oz_id)
            # o_zone_id does not exist in node.csv, discard it
            if oz_id not in zone_to_node_dict.keys():
                continue

            dz_id = int(dz_id)
            # d_zone_id does not exist in node.csv, discard it
            if dz_id not in zone_to_node_dict.keys():
                continue

            volume = float(volume)

            # set up total demand volume for an OD pair
            if (oz_id, dz_id) not in demands.keys():
                demands[(oz_id, dz_id)] = 0
            demands[(oz_id, dz_id)] += volume
            # set up volume for ColumnVec
            if (at, dp, oz_id, dz_id) not in column_pool.keys():
                column_pool[(at, dp, oz_id, dz_id)] = ColumnVec()
            column_pool[(at, dp, oz_id, dz_id)].od_vol += volume

            if volume == 0:
                continue

            total_agents += int(volume + 1)

    print(f"the number of agents is {total_agents}")


def _auto_setup(assignment):
    """ automatically set up one demand period and one agent type

    The two objects will be set up using the default construnctors using the
    default values. See class DemandPeriod and class AgentType for details
    """
    dp = DemandPeriod()
    at = AgentType()

    assignment.demand_periods.append(dp)
    assignment.agent_types.append(at)


def read_settings(input_dir, assignment):
    try:
        import yaml as ym

        with open(input_dir+'/settings.yml') as file:
            settings = ym.full_load(file)
            # demand files
            demands = settings['demand_files']
            for i, d in enumerate(demands):
                demand_file = d['file_name']
                # demand_format_tpye = d['format_type']
                demand_period = d['period']
                demand_time_period = d['time_period']
                demand_agent_type = d['agent_type']

                dp = DemandPeriod(i,
                                  demand_period,
                                  demand_time_period,
                                  demand_agent_type,
                                  demand_file)

                assignment.demand_periods.append(dp)

            # agent types
            agents = settings['agents']
            for i, a in enumerate(agents):
                agent_type = a['type']
                agent_name = a['name']
                agent_vot = a['vot']
                agent_flow_type = a['flow_type']
                agent_pce = a['pce']

                at = AgentType(i,
                               agent_type,
                               agent_name,
                               agent_vot,
                               agent_flow_type,
                               agent_pce)

                assignment.agent_types.append(at)
    except ImportError:
        # just in case user does not have pyyaml installed
        print('Please intall pyyaml next time!')
        print('Engine will set up one demand period and one agent type using '
              'default values for you, which might NOT reflect your case!\n')
        _auto_setup(assignment)
    except FileNotFoundError:
        # just in case user does not provide settings.yml
        print('Engine will set up one demand period and one agent type using '
              'default values for you, which might NOT reflect your case!\n')
        _auto_setup(assignment)
    except Exception as exception:
        raise exception


def output_columns(ui, output_dir='.'):
    with open(output_dir+'/agent.csv', 'w',  newline='') as fp:
        network = ui._base_assignment

        nodes = network.get_nodes()
        links = network.get_links()
        zones = network.get_zones()
        column_pool = network.get_column_pool()

        writer = csv.writer(fp)

        line = ['agent_id',
                'o_zone_id',
                'd_zone_id',
                'path_id',
                'agent_type',
                'demand_period',
                'volume',
                'toll',
                'travel_time',
                'distance',
                'node_sequence',
                'link_sequence',
                'geometry']

        writer.writerow(line)

        path_sep = ';'

        i = 0
        for oz_id in zones:
            for dz_id in zones:
                for at in network.get_agent_types():
                    for dp in network.get_demand_periods():
                        if (at.get_id(), dp.get_id(), oz_id, dz_id) not in column_pool.keys():
                            continue

                        cv = column_pool[(at.get_id(), dp.get_id(), oz_id, dz_id)]

                        for col in cv.get_columns().values():
                            i += 1
                            node_seq = path_sep.join(
                                str(nodes[x].get_node_id()) for x in reversed(col.nodes)
                            )
                            link_seq = path_sep.join(
                                str(links[x].get_link_id()) for x in reversed(col.links)
                            )
                            geometry = ', '.join(
                                nodes[x].get_coordinate() for x in reversed(col.nodes)
                            )
                            geometry = 'LINESTRING (' + geometry + ')'

                            line = [i,
                                    oz_id,
                                    dz_id,
                                    col.get_seq_no(),
                                    at.get_type(),
                                    dp.get_period(),
                                    col.get_volume(),
                                    col.get_toll(),
                                    col.get_travel_time(),
                                    col.get_distance(),
                                    node_seq,
                                    link_seq,
                                    geometry]

                            writer.writerow(line)


def output_link_performance(ui, output_dir='.'):
    with open(output_dir+'/link_performance.csv', 'w',  newline='') as fp:
        network = ui._base_assignment

        links = network.get_links()

        writer = csv.writer(fp)

        line = ['link_id',
                'from_node_id',
                'to_node_id',
                'time_period',
                'volume',
                'travel_time',
                'speed',
                'VOC',
                'queue',
                'density',
                'geometry',
                'notes']

        writer.writerow(line)

        for link in links:
            for dp in network.get_demand_periods():
                avg_travel_time = link.get_period_avg_travel_time(dp.get_id())
                speed = link.get_length() / (max(0.001, avg_travel_time) / 60)

                line = [link.get_link_id(),
                        link.get_from_node_id(),
                        link.get_to_node_id(),
                        dp.get_period(),
                        link.get_period_flow_vol(dp.get_id()),
                        avg_travel_time,
                        speed,
                        link.get_period_voc(dp.get_id()),
                        '',
                        '',
                        link.get_geometry(),
                        '']

                writer.writerow(line)


def read_network(load_demand='true', input_dir='.'):
    assignm = Assignment()
    network = Network()

    read_settings(input_dir, assignm)

    read_nodes(input_dir,
               network.node_list,
               network.internal_node_seq_no_dict,
               network.external_node_id_dict,
               network.zone_to_nodes_dict)

    read_links(input_dir,
               network.link_list,
               network.node_list,
               network.internal_node_seq_no_dict,
               assignm.get_agent_type_count(),
               assignm.get_demand_period_count())

    if load_demand:
        for at in assignm.get_agent_types():
            for dp in assignm.get_demand_periods():
                read_demand(input_dir,
                            dp.get_file_name(),
                            at.get_id(),
                            dp.get_id(),
                            network.zone_to_nodes_dict,
                            assignm.demands,
                            assignm.column_pool)

    network.update(assignm.get_agent_type_count(),
                   assignm.get_demand_period_count())

    assignm.network = network
    assignm.setup_spnetwork()

    ui = UI(assignm)

    return ui