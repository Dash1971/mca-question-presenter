(function (root) {
  'use strict';
  const numeric = /^[+-]?(?:\d+(?:\.\d*)?|\.\d+)$/;
  function normalize(value) {
    const text = String(value ?? '').trim().toLowerCase();
    return numeric.test(text) ? String(Number(text)) : text;
  }
  function answered(q, response = {}) {
    if (q.kind === 'single' || q.kind === 'multi') return (response.selected || []).length > 0;
    if (q.kind === 'fields') return q.fields.every((_, i) => String(response.fields?.[i] ?? '').trim() !== '');
    if (q.kind === 'match') return q.terms.every((_, i) => Number.isInteger(response.matches?.[i]));
    if (q.kind === 'place') return q.tokens.every(token => Array.isArray(response.points?.[token]));
    return false;
  }
  function grade(q, response = {}) {
    if (!answered(q, response)) return false;
    if (q.kind === 'single' || q.kind === 'multi') {
      const selected = response.selected || [];
      return selected.length === q.answer.length && new Set(selected).size === selected.length && q.answer.every(i => selected.includes(i));
    }
    if (q.kind === 'fields') {
      const key = q.answers || q.fields.map(field => field.answer);
      return key.every((value, i) => {
        const input = String(response.fields?.[i] ?? '').trim();
        const tolerance = q.fields[i].tolerance;
        if (Number.isFinite(tolerance) && numeric.test(input)) return Math.abs(Number(input) - Number(value)) <= tolerance + 1e-10;
        return normalize(input) === normalize(value);
      });
    }
    if (q.kind === 'match') return q.answers.every((value, i) => response.matches?.[i] === value);
    if (q.kind === 'place') return q.tokens.every(token => {
      const point = response.points?.[token], rect = q.targets?.[token];
      return point?.length === 2 && point.every(Number.isFinite) && rect && point[0] >= rect[0] && point[0] <= rect[2] && point[1] >= rect[1] && point[1] <= rect[3];
    });
    return false;
  }
  function result(paper, responses = {}) {
    const questions = paper.questions.filter(q => q.scored !== false);
    const correct = questions.filter(q => grade(q, responses[q.id])).length;
    return {correct, total: questions.length, percent: questions.length ? Math.round(correct / questions.length * 100) : 0};
  }
  const core = {normalize, answered, grade, result};
  if (typeof module !== 'undefined' && module.exports) module.exports = core;
  root.ExamCore = core;
})(typeof window === 'undefined' ? globalThis : window);
