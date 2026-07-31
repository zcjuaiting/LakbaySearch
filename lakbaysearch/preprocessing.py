import re
import string
from typing import List


STOP_WORDS: set = {
    'a', 'an', 'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
    'of', 'by', 'with', 'from', 'as', 'is', 'was', 'are', 'were', 'be',
    'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
    'would', 'could', 'should', 'may', 'might', 'shall', 'can', 'need',
    'dare', 'ought', 'used', 'it', 'its', 'it\'s', 'i', 'me', 'my',
    'we', 'our', 'you', 'your', 'he', 'him', 'his', 'she', 'her', 'they',
    'them', 'their', 'this', 'that', 'these', 'those', 'what', 'which',
    'who', 'whom', 'whose', 'when', 'where', 'why', 'how', 'all', 'each',
    'every', 'both', 'few', 'more', 'most', 'some', 'any', 'no', 'not',
    'only', 'own', 'same', 'so', 'than', 'too', 'very', 'just', 'because',
    'if', 'then', 'else', 'when', 'up', 'down', 'out', 'off', 'over',
    'under', 'again', 'further', 'once', 'here', 'there', 'about', 'above',
    'across', 'after', 'around', 'before', 'behind', 'between', 'below',
    'beneath', 'beside', 'beyond', 'during', 'inside', 'into', 'near',
    'onto', 'outside', 'through', 'throughout', 'toward', 'underneath',
    'until', 'upon', 'within', 'without', 'am', 'been', 'being', 'having',
    'doing', 'getting', 'going', 'saying', 'making', 'knowing', 'thinking',
    'seeing', 'taking', 'using', 'giving', 'finding', 'being', 'looking',
    'coming', 'going', 'trying', 'calling', 'letting', 'keeping', 'putting',
    'setting', 'running', 'moving', 'living', 'playing', 'turning', 'bringing',
    'beginning', 'continue', 'did', 'does', 'done', 'got', 'get', 'go',
    'goes', 'gone', 'know', 'knows', 'make', 'makes', 'made', 'take',
    'takes', 'took', 'taken', 'use', 'uses', 'used', 'using', 'see',
    'sees', 'saw', 'seen', 'come', 'comes', 'came', 'say', 'says', 'said',
    'find', 'finds', 'found', 'give', 'gives', 'gave', 'given', 'tell',
    'tells', 'told', 'think', 'thinks', 'thought', 'look', 'looks', 'looked',
    'call', 'calls', 'called', 'ask', 'asks', 'asked', 'need', 'needs',
    'needed', 'feel', 'feels', 'felt', 'become', 'becomes', 'became',
    'leave', 'leaves', 'left', 'put', 'puts', 'put', 'mean', 'means', 'meant',
    'let', 'lets', 'let', 'keep', 'keeps', 'kept', 'begin', 'begins', 'began',
    'begun', 'show', 'shows', 'showed', 'shown', 'hear', 'hears', 'heard',
    'watch', 'watches', 'watched', 'include', 'includes', 'included',
    'bring', 'brings', 'brought', 'write', 'writes', 'wrote', 'written',
    'provide', 'provides', 'provided', 'remove', 'removes', 'removed',
    'support', 'supports', 'supported', 'follow', 'follows', 'followed',
    'allow', 'allows', 'allowed', 'add', 'adds', 'added', 'change', 'changes',
    'changed', 'turn', 'turns', 'turned', 'start', 'starts', 'started',
    'try', 'tries', 'tried', 'stop', 'stops', 'stopped', 'hold', 'holds',
    'held', 'set', 'sets', 'setting', 'lead', 'leads', 'led', 'stand',
    'stands', 'stood', 'form', 'forms', 'formed', 'carry', 'carries',
    'carried', 'talk', 'talks', 'talked', 'open', 'opens', 'opened',
    'close', 'closes', 'closed', 'walk', 'walks', 'walked', 'want',
    'wants', 'wanted', 'work', 'works', 'worked', 'play', 'plays', 'played',
    'live', 'lives', 'lived', 'believe', 'believes', 'believed', 'happen',
    'happens', 'happened', 'seem', 'seems', 'seemed', 'help', 'helps',
    'helped', 'move', 'moves', 'moved', 'grow', 'grows', 'grew', 'grown',
    'learn', 'learns', 'learned', 'plan', 'plans', 'planned', 'note',
    'notes', 'noted', 'list', 'lists', 'listed', 'like', 'likes', 'liked',
    'also', 'well', 'back', 'still', 'even', 'much', 'while', 'never',
    'quite', 'rather', 'already', 'yet', 'just', 'really', 'almost',
    'enough', 'ever', 'always', 'however', 'though', 'although', 'since',
    'until', 'etc', 'eg', 'ie', 'vs', 'de', 'la', 'le', 'en', 'el', 'un',
    'una', 'los', 'las', 'del', 'con', 'por', 'para', 'mas', 'pero', 'que',
}


def lowercase(text: str) -> str:
    return text.lower()


def remove_punctuation(text: str) -> str:
    translator = str.maketrans('', '', string.punctuation)
    return text.translate(translator)


def normalize_whitespace(text: str) -> str:
    return re.sub(r'\s+', ' ', text).strip()


def remove_stop_words(tokens: List[str]) -> List[str]:
    return [token for token in tokens if token not in STOP_WORDS and len(token) > 1]


def tokenize(text: str) -> List[str]:
    return text.split()


def preprocess(text: str) -> str:
    text = lowercase(text)
    text = remove_punctuation(text)
    text = normalize_whitespace(text)
    tokens = tokenize(text)
    tokens = remove_stop_words(tokens)
    return ' '.join(tokens)