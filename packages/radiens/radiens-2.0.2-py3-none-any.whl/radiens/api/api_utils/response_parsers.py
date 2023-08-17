from radiens.grpc.common_pb2 import RadixFileTypes
from radiens.signal_group.SignalGroup import SignalGroup


def parse_CpRmMvLsReply(res):
    parsed_res = {
        'num_files': res.numFiles, 'num_dsource': res.numDsource,
        'num_bytes': res.numBytes, 'dest_path': res.destPath, 
        'msg': res.msg, 'data_source_info': {'descriptor': [], 'stat': []}}

    for dsource in res.dsource:
        parsed_res['data_source_info']['descriptor'].append({
            'path': dsource.desc.path, 'base_name': dsource.desc.baseName,
            'file_type': get_radix_file_type(dsource.desc.fileType)})
        parsed_res['data_source_info']['stat'].append({
            'num_files': dsource.stat.numFiles, 'num_bytes_primary_data': dsource.stat.numBytesPrimaryData,
            'num_bytes_meta_data': dsource.stat.numBytesMetaData, 'num_bytes': dsource.stat.numBytes, 'is_meta_data_file': dsource.stat.isMetadataFile, 
            'time_stamp': {'seconds': dsource.stat.timeStamp.seconds, 'nanos': dsource.stat.timeStamp.nanos},
            'num_channels': dsource.stat.numChannels, 'duration_sec': dsource.stat.durationSec, 
            'dataset_uid': dsource.stat.datasetUID, 'dataset_checksum': dsource.stat.datasetChecksum, 'sample_freq': dsource.stat.sampleRate})

    return parsed_res

def parse_data_source_set_save_reply(res):
    parsed_res = {
        'dsourceID': res.dsourceID, 'status': {
        'base_file_name': res.status.baseFileName, 'data_source_type': res.status.dataSourceType, 
        'duration': res.status.duration, 'file_type': res.status.fileType, 
        'label': res.status.label, 'mode': res.status.mode, 
        'num_total_samples': res.status.numTotalSamples, 'path': res.status.path, 
        'samp_freq': res.status.sampleFreq, 'shape': res.status.shape, 
        'signal_group': SignalGroup(res.status.signalGroup), 'size_bytes': res.status.sizeBytes, 
        'time_range': [res.status.timeRange[0], res.status.timeRange[1]], 'time_stamp_range': [res.status.timestampRange[0], res.status.timestampRange[1]], 
        'type': res.status.type, 'uid': res.status.uid}}
    return parsed_res

def get_radix_file_type(file_type):
    return RadixFileTypes.Name(file_type).lower()
