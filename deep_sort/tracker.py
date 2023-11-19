# vim: expandtab:ts=4:sw=4
from __future__ import absolute_import
import numpy as np
from . import kalman_filter
from . import linear_assignment
from . import iou_matching
from .track import Track


class Tracker:
    """
    This is the multi-target tracker.

    Parameters
    ----------
    metric : nn_matching.NearestNeighborDistanceMetric
        A distance metric for measurement-to-track association.
    max_age : int
        Maximum number of missed misses before a track is deleted.
    n_init : int
        Number of consecutive detections before the track is confirmed. The
        track state is set to `Deleted` if a miss occurs within the first
        `n_init` frames.

    Attributes
    ----------
    metric : nn_matching.NearestNeighborDistanceMetric
        The distance metric used for measurement to track association.
    max_age : int
        Maximum number of missed misses before a track is deleted.
    n_init : int
        Number of frames that a track remains in initialization phase.
    kf : kalman_filter.KalmanFilter
        A Kalman filter to filter target trajectories in image space.
    tracks : List[Track]
        The list of active tracks at the current time step.

    """

    def __init__(self, metric, max_iou_distance=0.8, max_age=15, n_init=3):
        self.metric = metric
        self.max_iou_distance = max_iou_distance
        self.max_age = max_age
        self.n_init = n_init

        self.kf = kalman_filter.KalmanFilter()
        self.tracks = []
        self._next_id = 1
        #Arunn
        self.dltracks =[] 
        self.trackframes={}
        #thanu
        self.dltracks2 =[]
        self.in_tracks = [] 
        #self.track_coords={}

    def predict(self):
        """Propagate track state distributions one time step forward.

        This function should be called once every time step, before `update`.
        """
        for track in self.tracks:
            track.predict(self.kf)

    def update(self, detections):
        """Perform measurement update and track management.

        Parameters
        ----------
        detections : List[deep_sort.detection.Detection]
            A list of detections at the current time step.

        """
        # Run matching cascade.
        matches, unmatched_tracks, unmatched_detections = \
            self._match(detections)

        # Update track set.
        # print("tracks", self.tracks)
        # print("before everything")
        # for track in self.tracks:
        #     print('track id : ', track.track_id)
        #     print('track status : ',track.state )
        #print(matches)
        for track_idx, detection_idx in matches:
            self.tracks[track_idx].update(
                self.kf, detections[detection_idx])
        for track_idx in unmatched_tracks:
            self.tracks[track_idx].mark_missed()
        for detection_idx in unmatched_detections:
            self._initiate_track(detections[detection_idx])

        # in_directions = ['Southwest','South','West'] #to store the in directions given by user initially
        # #this is added because to find the new deleted track ids
        # self.dltracks2 +=[t for t in self.tracks if t.is_deleted()]
        # for dltrack in self.dltracks2:
        #     if dltrack not in self.dltracks:
        #         if dltrack.previous_state == 2: #confirming whether the track is deleted after confirming
        #             if self.trackframes[int(dltrack.track_id)]['direction'] in in_directions:
        #                 self.in_tracks.append(dltrack) #adding the people track who are coming inside
        
        # for dltrack2 in self.dltracks2:
        #     print(dltrack2.track_id, end=" ")
        
        # print()
        # for dltrack in self.dltracks:
        #     print(dltrack.track_id, end=" ")

        # print()
        # print("length of intracks",len(self.in_tracks))
        # for intrack in self.in_tracks:
        #     print("intrack id : ", intrack.track_id)

        self.dltracks +=[t for t in self.tracks if t.is_deleted()]        
        self.tracks = [t for t in self.tracks if not t.is_deleted()]
        

        # Update distance metric.
        active_targets = [t.track_id for t in self.tracks if t.is_confirmed()]
        features, targets = [], []
        for track in self.tracks:
            if not track.is_confirmed():
                continue
            features += track.features
            targets += [track.track_id for _ in track.features]
            track.features = []
        self.metric.partial_fit(
            np.asarray(features), np.asarray(targets), active_targets)

    def _match(self, detections):

        def gated_metric(tracks, dets, track_indices, detection_indices):
            features = np.array([dets[i].feature for i in detection_indices])
            targets = np.array([tracks[i].track_id for i in track_indices])
            cost_matrix = self.metric.distance(features, targets)
            cost_matrix = linear_assignment.gate_cost_matrix(
                self.kf, cost_matrix, tracks, dets, track_indices,
                detection_indices)

            return cost_matrix

        # Split track set into confirmed and unconfirmed tracks.
        confirmed_tracks = [
            i for i, t in enumerate(self.tracks) if t.is_confirmed()]
        unconfirmed_tracks = [
            i for i, t in enumerate(self.tracks) if not t.is_confirmed()]

        # Associate confirmed tracks using appearance features.
        matches_a, unmatched_tracks_a, unmatched_detections = \
            linear_assignment.matching_cascade(
                gated_metric, self.metric.matching_threshold, self.max_age,
                self.tracks, detections, confirmed_tracks)

        # Associate remaining tracks together with unconfirmed tracks using IOU.
        iou_track_candidates = unconfirmed_tracks + [
            k for k in unmatched_tracks_a if
            self.tracks[k].time_since_update == 1]
        unmatched_tracks_a = [
            k for k in unmatched_tracks_a if
            self.tracks[k].time_since_update != 1]
        matches_b, unmatched_tracks_b, unmatched_detections = \
            linear_assignment.min_cost_matching(
                iou_matching.iou_cost, self.max_iou_distance, self.tracks,
                detections, iou_track_candidates, unmatched_detections)

        matches = matches_a + matches_b
        unmatched_tracks = list(set(unmatched_tracks_a + unmatched_tracks_b))
        return matches, unmatched_tracks, unmatched_detections

    def _initiate_track(self, detection):
        mean, covariance = self.kf.initiate(detection.to_xyah())
        min_x,min_y,max_x,max_y = detection.to_tlbr()
        class_name = detection.get_class()
        mid_x = (min_x + max_x)/2
        mid_y = (min_y + max_y)/2
        self.tracks.append(Track(
            mean, covariance, self._next_id, self.n_init, self.max_age,
            detection.feature, class_name))
        self.trackframes[self._next_id] ={1:1,2:"",'pts':[(mid_x,mid_y),(0,0)],'direction':"",'status':'undefined','init_sign':'undefined'}  #Arunn
        '''
        direction : stores inn which direction the persion is moving
        status : stores whether the persion comin in or out
        init_sign : it stores in which region person identified initially
        '''
        self._next_id += 1
