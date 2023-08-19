try:
    import torch
    BaseClass = torch.utils.data.sampler.BatchSampler
except ImportError:
    BaseClass = object

class EquiarealBatchSampler(BaseClass):
    """
    Most batch samplers keep the number of samples in a batch constant
    This one varies the number of samples to equalize the footprint of each batch instead.
    (number of samples x the length of each sample)

    sampler is an iterable of indices to be batched
    len_checker is a function that takes an index and returns the length of the sample at that index
    max_size is the maximum number of samples in a batch
    max_footprint is the maximum footprint of a batch
    """

    def __init__(self, sampler, len_checker, max_size, max_footprint):
        self.sampler = sampler
        self.len_checker = len_checker
        self.max_size = max_size
        self.max_footprint = max_footprint

    def __iter__(self):
        batch = []
        batch_footprint = 0

        for ix in self.sampler:
            length = self.len_checker(ix)
            expected_footprint = batch_footprint + length

            if expected_footprint > self.max_footprint or len(batch) >= self.max_size:
                yield batch
                batch = []
                batch_footprint = length
            else:
                batch_footprint = expected_footprint

            batch.append(ix) # ha ha

        yield batch

    def __len__(self):
        return None