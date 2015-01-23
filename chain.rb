class Chain
  def initialize(data)
    @data = Hash.new {Hash.new(0)}
    data.each do |post|
      parse_post post.map(&:downcase)
    end
  end


  def data
    @data
  end
  def get_next(wordlist)
    list = @data[fetchable(wordlist)]

    lista = []
    list.each do |item, count|
      lista += [item] * count
    end
    lista.sample
  end

  private

  def parse_post(post)
    post = ["^"] + post + ["$"]
    post.size.times do |index|
      hash = @data[post[range(index)].join(" ")]
      hash[post[index + 1]] += 1
      @data[post[range(index)].join(" ")] = hash
      if post[index + 1] == "$"
        return
      end
    end
  end

  def range(index)
    [index - 2, 0].max .. [index, 0].max
  end

  def fetchable(wordlist)
    (["^"] + wordlist)[range(wordlist.size)].join(" ")
  end

end

def test_chain
  ["hej då haha".split, "Hej du suger".split, "du suger fett".split, "du suger mer än din mamma".split]
end
