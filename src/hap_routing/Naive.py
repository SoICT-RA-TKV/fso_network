from src.utils.Distance import *
from copy import deepcopy
from collections import namedtuple

HAP = namedtuple('HAP', ['index', 'x', 'y'])
FLOW = namedtuple('FLOW', ['wavelength', 'nodes'])
EDGE = namedtuple('EDGE', ['u', 'v', 'w'])

class NaiveRouting:
	def __init__(self, berDict, berThreshold, W, C, hap, demands):
		self.berDict, self.berThreshold, self.W, self.C, self.hap, self.demands = \
			berDict, berThreshold, W, C, hap, demands

		self.NHAP_origin = demands.shape[0]
		self.NHAP_all = len(hap)
		self.remains = deepcopy(demands)
		self.capacities = np.array([C] * self.NHAP_all, dtype=int)

		self.dists = np.ndarray(shape=(self.NHAP_all, self.NHAP_all), dtype=float)
		self.bers = np.ndarray(shape=(self.NHAP_all, self.NHAP_all), dtype=float)

		for i in range(self.NHAP_all):
			for j in range(self.NHAP_all):
				self.dists[i, j] = distance(hap[i], hap[j])
				# print(dists[i, j])
				self.bers[i, j] = hap_ber(self.dists[i, j], berDict)

		self.flows = set()
		self.used_edges = set()
		self.used_links = set()
		self.response_list = set()

	def forbid_link(self, iu, iv):
		self.used_links.add((iu, iv))
		self.used_links.add((iv, iu))

	def decrease_capacity(self, ih, c):
		self.capacities[ih] -= 1

	def solve(self):
		berDict, berThreshold, W, C, hap, demands = \
			self.berDict, self.berThreshold, self.W, self.C, self.hap, self.demands
		NHAP_origin, NHAP_all, remains, capacities = self.NHAP_origin, self.NHAP_all, self.remains, self.capacities
		dists, bers = self.dists, self.bers
		flows, used_edges, used_links, response_list = self.flows, self.used_edges, self.used_links, self.response_list
		
		while True:
			u = np.argmax([0 if i in response_list else sum(remains[i, :]) + sum(remains[:, i]) for i in range(NHAP_origin)])
			# print('u:', u)
			if (sum(remains[u, :]) + sum(remains[:, u]) == 0) or (u in response_list):
				# print(response_list)
				break
			response_list.add(u)
			V = [v for v in range(NHAP_origin) if (remains[u, v] + remains[v, u] > 0) and (capacities[v] > 1)]
			children = dict()
			children[u] = set()
			parent = dict()
			parent[u] = u
			e2e_ber = dict()
			e2e_ber[u] = 0
			leaves = set()

			# Xay dung cay goc u
			while (len(V) > 0) and (capacities[u] > 0):
				tmp_dist = [distance(hap[u], hap[i]) * (float('inf') if (u, i) in used_links else 1) for i in V]
				ik = np.argmin(tmp_dist)
				k = V[ik]
				if (tmp_dist[ik] == float('inf')):
					break
				else:
					V.remove(k)
					children[u].add(k)
					parent[k] = u
					children[k] = set()
					e2e_ber[k] = bers[u, k]
					capacities[u] -= 1
					capacities[k] -= 1
					out_demands = remains[u, k]
					in_demands = remains[k, u]
					leaves.add(k)
					# Xay dung tiep nhanh k
					while len(V) > 0:
						tmp_dist = [distance(hap[k], hap[i]) * (float("inf") if (k, i) in used_links else 1) for i in V]
						iv = np.argmin(tmp_dist)
						v = V[iv]
						if (tmp_dist[iv] == float('inf')) or (out_demands + demands[u, v] > W) or (in_demands + demands[v, u] > W):
							break
						else:
							V.remove(v)
							children[k] = set([v])
							parent[v] = k
							children[v] = set()
							e2e_ber[v] = e2e_ber[k] + bers[k, v]
							capacities[k] -= 1
							capacities[v] -= 1
							out_demands += demands[u, v]
							in_demands += demands[v, u]
							leaves.discard(k)
							leaves.add(v)
							k = v
							continue
					continue

			num_add_hap = dict()
			for iu in children:
				for iv in children[iu]:
					num_add_hap[(iu, iv)] = 0
			for l in leaves:
				list_link = []
				v = l
				u = parent[v]
				while u != v:
					list_link.append((u, v))
					v = u
					u = parent[v]
				while e2e_ber[l] > berThreshold:
					cur_err = np.array([(num_add_hap[link] + 1) * hap_ber(distance(hap[link[0]], hap[link[1]]) / (num_add_hap[link] + 1), berDict) for link in list_link])
					prm_err = np.array([(num_add_hap[link] + 2) * hap_ber(distance(hap[link[0]], hap[link[1]]) / (num_add_hap[link] + 2), berDict) for link in list_link])
					gain = cur_err - prm_err
					max_gain = np.argmax(gain)
					num_add_hap[list_link[max_gain]] += 1
					e2e_ber[l] -= gain[max_gain]
			
			for link in num_add_hap:
				iu = link[0]
				iv = link[1]
				delta = [(hap[iv].x - hap[iu].x) / (num_add_hap[(iu, iv)] + 1), (hap[iv].y - hap[iu].y) / (num_add_hap[(iu, iv)] + 1)]
				for i in range(num_add_hap[link]):
					hap.append(HAP(NHAP_all, hap[iu].x + delta[0], hap[iu].y + delta[1]))
					ik = NHAP_all
					NHAP_all += 1
					used_links.add((iu, ik))
					used_links.add((ik, iu))
					children[iu].discard(iv)
					children[iu].add(ik)
					children[ik] = set([iv])
					parent[iv] = ik
					parent[ik] = iu
					iu = ik
				used_links.add((iu, iv))
				used_links.add((iv, iu))

			self.route(children, u, NHAP_origin, remains, flows, used_edges, used_links)
		# print(flows)
		# print(remains)
		# print(sum(sum(remains)) / sum(sum(demands)))
		# print(len(used_links))
		# print(len(used_edges))
		# print(NHAP_w)
		# print(capacities)
		# print(used_links)
		# if sum(sum(demands)) > 0:
		# 	synthesis_file = open('synthesis_d15.csv', 'a')
		# 	synthesis_file.write(joinany([file.split('_')[1], max(h.x for h in hap) - min(h.x for h in hap), max(h.y for h in hap) - min(h.y for h in hap),
		# 		sum(sum(demands)), NHAP, NHAP_w, len(used_links), len(used_edges), sum(sum(remains)),
		# 		1 - sum(sum(remains)) / sum(sum(demands)), len(used_edges) / NHAP_w, len(used_edges) / (len(used_links) * 128),
		# 		int(file.split('_')[1]) / NHAP, sum(sum(demands)) / NHAP, sum(sum(dists)) / (NHAP * NHAP)], ',') + '\n')
		# 	synthesis_file.close()
		return flows, used_edges, used_links

	def route(self, children, u, NHAP, remains, flows, used_edges, used_links):
		# print(u)
		for k in children[u]:
			h = k
			w_out = 0
			w_in = 0
			nodes = [u]
			while True:
				nodes.append(k)
				if u < NHAP and k < NHAP:
					# print(u, k, NHAP)
					while (remains[u, k] > 0) and (w_out < 128):
						new_flow = FLOW(w_out, tuple(nodes))
						if self.check_flow(new_flow, used_links, used_edges):
							# print(new_flow)
							self.add_flow(new_flow, flows, used_edges)
							remains[u, k] -= 1
						w_out += 1
					while (remains[k, u] > 0) and (w_in < 128):
						new_flow = FLOW(w_in, tuple(nodes[::-1]))
						if self.check_flow(new_flow, used_links, used_edges):
							# print(new_flow)
							self.add_flow(new_flow, flows, used_edges)
							remains[k, u] -= 1
						w_in += 1
				if len(children[k]) == 0:
					break
				else:
					k = list(children[k])[0]
			self.route(children, h, NHAP, remains, flows, used_edges, used_links)

	def check_flow(self, flow, used_links, used_edges):
		for i in range(len(flow.nodes) - 1):
			if ((flow.nodes[i], flow.nodes[i + 1]) not in used_links) or (EDGE(flow.nodes[i], flow.nodes[i + 1], flow.wavelength) in used_edges):
				return False
		return True

	def add_flow(self, flow, flows, used_edges):
		flows.add(flow)
		for i in range(len(flow.nodes) - 1):
			used_edges.add(EDGE(flow.nodes[i], flow.nodes[i + 1], flow.wavelength))