use std::collections::HashMap;

use pyo3::prelude::*;

const KEYWORDS: [char; 4] = ['*', '_', '~', '`'];
const NO_SUB_PARSING_KEYWORDS: [char; 1] = ['`'];
const QUOTE_KEYWORDS: [char; 1] = ['>'];
const PLACEHOLDER: &str = "\u{200B}\u{200B}\u{200B}\u{200B}\u{200B}\u{200B}\u{200B}\u{200B}\u{200B}\u{200B}";

#[pyfunction]
fn format_body(body: String, new_tags: HashMap<String, (String, String)>) -> PyResult<String> {
    let mut chars: Vec<char> = body.chars().collect();
    if chars.len() < 1 {
        return Ok(body);
    }
    let styles: Vec<(String, usize, usize, usize, usize)> = parse_with_limits(&chars, 0, chars.len() - 1, 0);
    let parse_quotes = new_tags.contains_key(&">".to_string());

    let mut tags: Vec<(usize, String, usize)> = vec![];
    for style in styles {
        let (keyword, start, remove_start, end, remove_end) = style;
        if new_tags.contains_key(&keyword) {
            let opening_tag = if keyword == "```language" {
                new_tags.get(&keyword).unwrap().0.clone()
                .replace("{}", &chars[start+3..remove_start-1]
                .into_iter()
                .collect::<String>())
            } else {
                new_tags.get(&keyword).unwrap().0.clone()
            };
            tags.push((start, opening_tag, remove_start));
            tags.push((end, new_tags.get(&keyword).unwrap().1.clone(), remove_end));
        } else if keyword == ">>" && parse_quotes {
            tags.push((start, "".to_string(), start+1));
        }
    }

    tags.sort_by(|a, b| b.0.cmp(&a.0));

    for tag in tags {
        let (index, tag, end) = tag;
        chars = [chars[..index].to_vec(), tag.chars().collect(), chars[end..].to_vec()].concat();
    }

    let text: String = if new_tags.contains_key("\n") {
        chars.into_iter().collect::<String>().replace("\n", &new_tags.get(&"\n".to_string()).unwrap().0)
    } else {
        chars.into_iter().collect::<String>()
    };

    Ok(remove_non_escaped_backslashes(text))
}

fn remove_non_escaped_backslashes(text: String) -> String {
    let tmp_string = text.replace("\\\\", PLACEHOLDER);
    let tmp_string = tmp_string.replace("\\", "");
    tmp_string.replace(PLACEHOLDER, "\\")
}

fn parse_with_limits(chars: &Vec<char>, start: usize, end: usize, depth: usize) -> Vec<(String, usize, usize, usize, usize)> {
    let mut styles = Vec::new();
    let mut index = start;
    let end = end.min(chars.len() - 1);

    while index <= end {
        if preceeded_by_backslash(chars, index, start) {
            index += 1;
            continue;
        }

        let c = chars[index];
        if QUOTE_KEYWORDS.contains(&c) {
            if is_quote_start(chars, index, depth) {
                let to = seek_end_of_quote(chars, index, end, depth);
                styles.push((">".to_string(), index, index + 1, to, to));
                styles.append(&mut parse_with_limits(chars, index + 1, to, depth + 1));
                index = to;
                continue;
            }
            if is_nested_quote(chars, index, depth) {
                styles.push((">>".to_string(), index, index + 1, index + 1, index + 1));
            }
            index += 1;
            continue;
        }

        if c == '`' && is_char_repeating(chars, c, 2, index + 1, end) {
            let end_of_line = seek_end_of_line(chars, index + 1, end);
            if end_of_line == end {
                index += 3;
                continue;
            }
            match seek_end_block(chars, c, end_of_line, end, depth) {
                Some(to) => {
                    println!("to {}", to);
                    if to != index + 3 && is_quote_start(chars, index, depth) {
                        let keyword = if end_of_line == index + 3 {
                            "```".to_string()
                        } else {
                            "```language".to_string()
                        };
                        let remove_end = if depth > 0 && (to == end || to == chars.len()) {
                            to
                        } else {
                            to + 4 + depth
                        };
                        styles.push((keyword, index, end_of_line + 1, to, remove_end));
                        styles.append(&mut parse_quotes_in_code_block(chars, index + 3, to, depth));
                        index = to;
                    }
                }
                None => ()
            }
            index += 3;
            continue;
        }

        if !preceeded_by_whitespace(chars, index, start) || followed_by_whitespace(chars, index, end) {
            index += 1;
            continue;
        }

        if c == '|' && is_char_repeating(chars, c, 1, index + 1, end) {
            match seek_end(chars, c, index + 2, 1, end) {
                Some(to) => {
                    if to != index + 2 {
                        let keyword = "||".to_string();
                        styles.push((keyword, index, index + 2, to, to + 2));
                        styles.append(&mut parse_with_limits(chars, index + 2, to - 1, depth));
                    }
                    index = to + 2;
                    continue;
                }
                None => ()
            }
            index += 2;
            continue;
        }

        if !KEYWORDS.contains(&c) {
            index += 1;
            continue;
        }

        match seek_end(chars, c, index + 1, 0, end) {
            Some (to) => {
                if to != index + 1 {
                    styles.push((c.to_string(), index, index + 1, to, to + 1));
                    if !NO_SUB_PARSING_KEYWORDS.contains(&c) {
                        styles.append(&mut parse_with_limits(chars, index + 1, to - 1, depth));
                    }
                }
                index = to;
            }
            None => ()
        }
        index += 1;
    }
    styles
}

fn parse_quotes_in_code_block(chars: &Vec<char>, start: usize, end: usize, depth: usize) -> Vec<(String, usize, usize, usize, usize)> {
    let mut quotes = Vec::new();
    let mut index = start;
    let end = end.min(chars.len() - 1);

    if depth < 1 {
        return quotes;
    }

    while index <= end {
        let c = chars[index];
        if QUOTE_KEYWORDS.contains(&c) {
            if is_nested_quote(chars, index, depth) {
                quotes.push((">>".to_string(), index, index + 1, index + 1, index + 1));
            }
            index += 1;
            continue;
        }
        index += 1;
    }
    quotes
}

fn is_nested_quote(chars: &Vec<char>, start: usize, depth: usize) -> bool {
    let mut index = start;
    let mut count = 0;

    while index > 0 {
        if chars[index] == '\n' {
            return true;
        }
        if !QUOTE_KEYWORDS.contains(&chars[index]) {
            return false;
        }
        count += 1;
        if count > depth {
            return false;
        }
        index -= 1;
    }
    true
}

fn is_char_repeating(chars: &Vec<char>, keyword: char, repetitions: usize, index: usize, end: usize) -> bool {
    (0..repetitions as usize)
        .all(|i| index + i <= end && chars[index + i] == keyword)
}

fn preceeded_by_whitespace(chars: &Vec<char>, index: usize, start: usize) -> bool {
    index == start || chars[index - 1].is_whitespace()
}

fn followed_by_whitespace(chars: &Vec<char>, index: usize, end: usize) -> bool {
    index >= end || chars[index + 1].is_whitespace()
}

fn seek_end(chars: &Vec<char>, keyword: char, start: usize, repetitions: usize, end: usize) -> Option<usize> {
    for i in start..=end {
        let c = chars[i];
        if c == '\n' {
            return None;
        }
        if c == keyword
            && !chars[i - 1].is_whitespace()
            && !preceeded_by_backslash(chars, i, start)
            && is_char_repeating(chars, keyword, repetitions, i + 1, end)
        {
            match seek_higher_order_end(chars, c, i + 1, repetitions, end) {
                Some(higher_order_i) => {
                    return Some(higher_order_i);
                }
                None => {
                    return Some(i);
                }
            }
        }
    }
    None
}

fn seek_higher_order_end(chars: &Vec<char>, keyword: char, start: usize, repetitions: usize, end: usize) -> Option<usize> {
    for i in start..=end {
        let c = chars[i];
        if c == '\n' {
            return None;
        }
        if c == keyword
            && chars[i - 1].is_whitespace()
            && !followed_by_whitespace(chars, i, end)
            && is_char_repeating(chars, keyword, repetitions, i + 1, end)
        {
            return None; // "*bold* *<--- beginning of new bold>*"
        }
        if c == keyword
            && !chars[i - 1].is_whitespace()
            && followed_by_whitespace(chars, i, end)
            && !preceeded_by_backslash(chars, i, start)
            && is_char_repeating(chars, keyword, repetitions, i + 1, end)
        {
            return Some(i);
        }
    }
    None
}

fn seek_end_of_line(chars: &Vec<char>, start: usize, end: usize) -> usize {
    chars[start..=end]
        .iter()
        .enumerate()
        .find(|&(_, &c)| c == '\n')
        .map_or(end + 1, |(i, _)| start + i)
}

fn seek_end_of_quote(chars: &Vec<char>, start: usize, end: usize, depth: usize) -> usize {
    for i in start..=end {
        if chars[i] == '\n' {
            if i + 2 + depth > chars.len() {
                return i;
            }
            if chars[i + 1..=i + 1 + depth].iter().any(|&c| !QUOTE_KEYWORDS.contains(&c)) {
                return i;
            }
        }
    }
    end + 1
}

fn seek_end_block(chars: &Vec<char>, keyword: char, start: usize, end: usize, depth: usize) -> Option<usize> {
    for i in start..=end {
        if chars[i] == '\n' {
            if i + depth == end && chars[i + 1..i + 1 + depth].iter().all(|&c| QUOTE_KEYWORDS.contains(&c)) {
                continue;
            }
            if i + 1 + depth > end {
                return Some(i);
            }
            if i + 4 + depth > end
                && chars[i + 1..i + 1 + depth].iter().all(|&c| QUOTE_KEYWORDS.contains(&c))
                && chars[i + 1 + depth] == keyword
                && is_char_repeating(chars, keyword, 2, i + 1 + depth, end)
            {
                return Some(i);
            }
        }
    }
    if end == chars.len() - 1 {
        if depth == 0 {
            return None;
        }
        return Some(chars.len());
    }
    Some(end)
}

fn is_quote_start(chars: &Vec<char>, index: usize, depth: usize) -> bool {
    index - depth == 0 || chars[index - 1 - depth] == '\n'
}

fn preceeded_by_backslash(chars: &Vec<char>, index: usize, start: usize) -> bool {
    if index == start {
        return false;
    }
    let mut num_backslashes = 0;
    while index > num_backslashes && chars[index - 1 - num_backslashes] == '\\' {
        num_backslashes += 1;
    }
    num_backslashes % 2 == 1
}

#[pymodule]
fn slidge_style_parser(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(format_body, m)?)?;
    Ok(())
}
