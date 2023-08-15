# (C) Copyright 2021 ECMWF.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.
#

import logging

from climetlab.vocabularies import VOCABULARIES

LOG = logging.getLogger(__name__)


def normalise_string(key, convention="cf"):
    vocabulary = VOCABULARIES[convention]

    new = vocabulary.normalise(key)
    LOG.debug(f"Normalising '{key}' into '{new}' ({convention} convention)")
    return new
